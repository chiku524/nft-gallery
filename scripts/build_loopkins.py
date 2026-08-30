#!/usr/bin/env python3
"""Paint Loopkins APNG trait layers and bake sample tokens.

Every trait is a 12-frame APNG on a shared 512 canvas and 80ms clock.
Character layers share one bob so a stacked preview stays locked together.
Sky, aura, and charm move on their own loops.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
TRAIT_DIR = ROOT / "public" / "traits"
BRAND_DIR = ROOT / "public" / "brand"
PREVIEW_DIR = ROOT / "public" / "generated-preview"
META_DIR = ROOT / "public" / "metadata"
ICON_PATH = ROOT / "src" / "app" / "icon.png"

SIZE = 512
FRAMES = 12
DURATION_MS = 80
H, W = SIZE, SIZE

HEAD = (256.0, 236.0)
HEAD_R = 96.0


def clamp01(x: np.ndarray | float) -> np.ndarray | float:
    return np.clip(x, 0.0, 1.0)


def smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = clamp01((x - edge0) / (edge1 - edge0))
    return t * t * (3.0 - 2.0 * t)


def rgb(hex_color: str) -> np.ndarray:
    value = hex_color.lstrip("#")
    return np.array([int(value[i : i + 2], 16) / 255.0 for i in (0, 2, 4)], dtype=np.float32)


def mix(a: np.ndarray | float, b: np.ndarray | float, t: float | np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    t = np.asarray(t, dtype=np.float32)
    if t.ndim >= 2 and a.ndim == 1:
        t = t[..., None]
    return a * (1.0 - t) + b * t


def blank() -> np.ndarray:
    return np.zeros((H, W, 4), dtype=np.float32)


def grid() -> tuple[np.ndarray, np.ndarray]:
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return xx, yy


def over(dst: np.ndarray, src: np.ndarray) -> None:
    sa = src[..., 3:4]
    da = dst[..., 3:4]
    out_a = sa + da * (1.0 - sa)
    rgb_out = src[..., :3] * sa + dst[..., :3] * da * (1.0 - sa)
    dst[..., :3] = np.divide(rgb_out, out_a, out=np.zeros_like(rgb_out), where=out_a > 1e-6)
    dst[..., 3:4] = out_a


def disc(
    dst: np.ndarray,
    cx: float,
    cy: float,
    r: float,
    color: np.ndarray,
    opacity: float = 1.0,
    soft: float = 1.6,
) -> None:
    xx, yy = grid()
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = smoothstep(r + soft, r - soft, d) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def ellipse(
    dst: np.ndarray,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    color: np.ndarray,
    opacity: float = 1.0,
    soft: float = 1.4,
) -> None:
    xx, yy = grid()
    d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    a = smoothstep(1.0 + soft / max(rx, ry), 1.0 - soft / max(rx, ry), d) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def glow(dst: np.ndarray, cx: float, cy: float, r: float, color: np.ndarray, opacity: float) -> None:
    xx, yy = grid()
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = np.exp(-0.5 * (d / r) ** 2) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def rect(
    dst: np.ndarray,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    color: np.ndarray,
    opacity: float = 1.0,
    radius: float = 0.0,
) -> None:
    xx, yy = grid()
    if radius <= 0:
        mask = (xx >= x0) & (xx <= x1) & (yy >= y0) & (yy <= y1)
        layer = blank()
        layer[..., :3] = color
        layer[..., 3] = mask.astype(np.float32) * opacity
        over(dst, layer)
        return
    cx = np.clip(xx, x0 + radius, x1 - radius)
    cy = np.clip(yy, y0 + radius, y1 - radius)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = smoothstep(radius + 1.2, radius - 1.2, d) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def star(dst: np.ndarray, cx: float, cy: float, r: float, color: np.ndarray, opacity: float, points: int = 5) -> None:
    xx, yy = grid()
    ang = np.arctan2(yy - cy, xx - cx)
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    inner = r * 0.42
    wave = np.cos(ang * points)
    edge = mix(np.float32(inner), np.float32(r), (wave + 1.0) * 0.5)
    a = smoothstep(edge + 1.4, edge - 1.4, dist) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def to_image(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(arr * 255.0, 0, 255).astype(np.uint8), "RGBA")


def save_apng(frames: list[Image.Image], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    stamped = []
    for index, frame in enumerate(frames):
        copy = frame.convert("RGBA")
        pixels = copy.load()
        r, g, b, a = pixels[0, 0]
        pixels[0, 0] = (r, g, b, max(a, 1) if a == 0 else a)
        pixels[1, 0] = (index, 0, FRAMES, 1)
        stamped.append(copy)
    stamped[0].save(
        path,
        save_all=True,
        append_images=stamped[1:],
        duration=[DURATION_MS] * len(stamped),
        loop=0,
        format="PNG",
        disposal=1,
        blend=0,
    )


def save_png(arr: np.ndarray, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    to_image(arr).save(path)


def bob(frame: int, amp: float = 5.0) -> float:
    return math.sin(2 * math.pi * frame / FRAMES) * amp


def phase(frame: int) -> float:
    return 2 * math.pi * frame / FRAMES


# --- skies ------------------------------------------------------------------

def sky_midnight(frame: int) -> np.ndarray:
    xx, yy = grid()
    t = phase(frame)
    top = rgb("0b1024")
    bot = rgb("1b2a4a")
    arr = blank()
    arr[..., :3] = mix(top, bot, yy / SIZE)
    arr[..., 3] = 1.0
    glow(arr, 256 + math.sin(t) * 18, 90, 160, rgb("6d8cff"), 0.22 + 0.06 * math.sin(t))
    rng = np.random.default_rng(11)
    for i in range(42):
        x = float(rng.uniform(12, 500))
        y = float(rng.uniform(12, 300))
        tw = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t + i * 0.7))
        disc(arr, x, y, 1.2 + (i % 3) * 0.4, rgb("f4f1ff"), tw, soft=1.1)
    return arr


def sky_neon(frame: int) -> np.ndarray:
    xx, yy = grid()
    t = phase(frame)
    arr = blank()
    arr[..., :3] = mix(rgb("070816"), rgb("12162c"), yy / SIZE)
    arr[..., 3] = 1.0
    pulse = 0.18 + 0.12 * (0.5 + 0.5 * math.sin(t))
    for n in range(10):
        y = 40 + n * 48 + math.sin(t + n) * 2
        rect(arr, 0, y, SIZE, y + 1.6, rgb("49f2c2"), pulse * (0.4 + n / 14), radius=0)
        x = 28 + n * 52 + math.cos(t * 0.6) * 4
        rect(arr, x, 0, x + 1.6, SIZE, rgb("ff5d8f"), pulse * 0.45, radius=0)
    glow(arr, 256, 420, 220, rgb("2de1c2"), 0.16)
    return arr


def sky_dawn(frame: int) -> np.ndarray:
    yy = grid()[1]
    t = phase(frame)
    arr = blank()
    arr[..., :3] = mix(rgb("ffb38a"), mix(rgb("ffd6e8"), rgb("7fb3ff"), yy / SIZE), yy / SIZE)
    arr[..., 3] = 1.0
    sun_y = 168 + math.sin(t) * 6
    glow(arr, 360, sun_y, 90, rgb("fff1c2"), 0.55)
    disc(arr, 360, sun_y, 38, rgb("ffe7a3"), 0.95, soft=2.2)
    return arr


def sky_forest(frame: int) -> np.ndarray:
    xx, yy = grid()
    t = phase(frame)
    arr = blank()
    arr[..., :3] = mix(rgb("0d1f18"), rgb("1d3d2a"), yy / SIZE)
    arr[..., 3] = 1.0
    for i, x in enumerate((70, 150, 250, 340, 430, 500)):
        h = 220 + (i % 3) * 40
        ellipse(arr, x, 520, 70, h, rgb("0a281c"), 0.55, soft=4)
    rng = np.random.default_rng(4)
    for i in range(18):
        x = float(rng.uniform(20, 490))
        y = 80 + (i * 37 + math.sin(t + i) * 18) % 280
        glow(arr, x, y, 7, rgb("d6ff7a"), 0.35 + 0.25 * math.sin(t + i))
    return arr


def sky_coral(frame: int) -> np.ndarray:
    yy = grid()[1]
    t = phase(frame)
    arr = blank()
    wash = 0.5 + 0.5 * math.sin(t * 0.5)
    arr[..., :3] = mix(rgb("2a1030"), mix(rgb("c45c4a"), rgb("f0a36b"), wash), yy / SIZE)
    arr[..., 3] = 1.0
    glow(arr, 120 + math.cos(t) * 20, 80, 140, rgb("ff8a6b"), 0.28)
    glow(arr, 400, 360, 180, rgb("6b2d4a"), 0.22)
    return arr


def sky_void(frame: int) -> np.ndarray:
    xx, yy = grid()
    t = phase(frame)
    arr = blank()
    arr[..., :3] = mix(rgb("05050a"), rgb("161022"), yy / SIZE)
    arr[..., 3] = 1.0
    rng = np.random.default_rng(21)
    for i in range(70):
        x = (float(rng.uniform(0, SIZE)) + math.cos(t + i) * 8) % SIZE
        y = (float(rng.uniform(0, SIZE)) + frame * (0.6 + i % 3) * 0.4) % SIZE
        disc(arr, x, y, 0.9, rgb("e8e0ff"), 0.25 + 0.5 * ((i + frame) % 5) / 5, soft=0.9)
    return arr


def sky_candy(frame: int) -> np.ndarray:
    xx, yy = grid()
    t = phase(frame)
    arr = blank()
    arr[..., :3] = mix(rgb("ffd0ea"), rgb("c8f4ff"), (xx + yy) / (SIZE * 2))
    arr[..., 3] = 1.0
    for i, (x, y, c) in enumerate(((120, 140, "ff9ad5"), (390, 200, "8ce0ff"), (240, 80, "ffe38a"))):
        glow(arr, x + math.sin(t + i) * 16, y + math.cos(t + i) * 10, 70, rgb(c), 0.35)
    return arr


def sky_storm(frame: int) -> np.ndarray:
    yy = grid()[1]
    t = phase(frame)
    arr = blank()
    arr[..., :3] = mix(rgb("14102a"), rgb("3a2f6b"), yy / SIZE)
    arr[..., 3] = 1.0
    flash = 0.55 if frame in (3, 8) else 0.0
    glow(arr, 300, 40, 200, rgb("d7c7ff"), 0.12 + flash)
    if flash:
        rect(arr, 250, 0, 262, 210, rgb("f4eeff"), 0.55)
        rect(arr, 258, 180, 310, 188, rgb("f4eeff"), 0.4)
    glow(arr, 160, 480, 160, rgb("6b4bff"), 0.18)
    return arr


SKIES = {
    "midnight": sky_midnight,
    "neon": sky_neon,
    "dawn": sky_dawn,
    "forest": sky_forest,
    "coral": sky_coral,
    "void": sky_void,
    "candy": sky_candy,
    "storm": sky_storm,
}


# --- auras ------------------------------------------------------------------

AURA_COLORS = {
    "mint": rgb("49f2c2"),
    "gold": rgb("ffd36a"),
    "magenta": rgb("ff5d8f"),
    "ice": rgb("8ce0ff"),
    "ember": rgb("ff7a3d"),
    "pixel": rgb("c6f24a"),
}


def paint_aura(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    t = phase(frame)
    color = AURA_COLORS[kind]
    pulse = 0.28 + 0.16 * (0.5 + 0.5 * math.sin(t))
    cx, cy = HEAD
    if kind == "gold":
        for r, op in ((168, pulse * 0.45), (148, pulse * 0.25)):
            # ring: outer disc minus inner
            tmp = blank()
            disc(tmp, cx, cy + 18, r, color, op, soft=4)
            disc(tmp, cx, cy + 18, r - 16, np.array([0, 0, 0], dtype=np.float32), 1.0, soft=3)
            # punch hole by resetting alpha in center
            xx, yy = grid()
            d = np.sqrt((xx - cx) ** 2 + (yy - cy - 18) ** 2)
            tmp[..., 3] *= smoothstep(r - 22, r - 8, d)
            over(arr, tmp)
        return arr
    if kind == "pixel":
        rng = np.random.default_rng(9)
        for i in range(28):
            x = cx + float(rng.uniform(-110, 110))
            y = cy + 20 + float(rng.uniform(-90, 120))
            s = 5 + (i % 3) * 3
            op = pulse * (0.4 + 0.6 * (0.5 + 0.5 * math.sin(t + i)))
            rect(arr, x, y, x + s, y + s, color, op, radius=1)
        return arr
    glow(arr, cx, cy + 24, 150 + 10 * math.sin(t), color, pulse)
    glow(arr, cx, cy + 40, 90, color, pulse * 0.55)
    return arr


# --- bodies -----------------------------------------------------------------

BODIES = {
    "pudding": {"fill": rgb("f3d2b3"), "shade": rgb("e0b48d"), "ear": None},
    "fox": {"fill": rgb("ff8b5c"), "shade": rgb("d96a3f"), "ear": "point"},
    "owl": {"fill": rgb("6b6aa8"), "shade": rgb("4e4d86"), "ear": "tuft"},
    "frog": {"fill": rgb("7ed957"), "shade": rgb("4ea336"), "ear": "nub"},
    "cat": {"fill": rgb("2a2430"), "shade": rgb("151218"), "ear": "tri"},
    "beetle": {"fill": rgb("1f6b68"), "shade": rgb("124844"), "ear": "horn"},
}


def paint_body(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    spec = BODIES[kind]
    fill, shade = spec["fill"], spec["shade"]
    dy = bob(frame)
    cx, cy = HEAD[0], HEAD[1] + dy
    # drop shadow
    ellipse(arr, cx, 430 + dy * 0.25, 92, 18, rgb("000000"), 0.18, soft=6)
    # torso
    ellipse(arr, cx, cy + 118, 78, 70, shade, 1.0, soft=2.2)
    ellipse(arr, cx, cy + 108, 70, 62, fill, 1.0, soft=2.0)
    # head
    glow(arr, cx, cy, 78, fill, 0.2)
    disc(arr, cx, cy, HEAD_R, fill, 1.0, soft=2.0)
    disc(arr, cx - 22, cy - 18, 42, mix(fill, rgb("ffffff"), 0.22), 0.55, soft=3)
    disc(arr, cx + 18, cy + 28, 36, shade, 0.22, soft=4)
    ear = spec["ear"]
    if ear == "point":
        ellipse(arr, cx - 70, cy - 78, 22, 38, fill, 1.0, soft=1.6)
        ellipse(arr, cx + 70, cy - 78, 22, 38, fill, 1.0, soft=1.6)
        ellipse(arr, cx - 70, cy - 74, 10, 20, rgb("ffd1c2"), 0.9, soft=1.2)
        ellipse(arr, cx + 70, cy - 74, 10, 20, rgb("ffd1c2"), 0.9, soft=1.2)
    elif ear == "tuft":
        ellipse(arr, cx - 48, cy - 92, 16, 28, fill, 1.0, soft=1.4)
        ellipse(arr, cx + 48, cy - 92, 16, 28, fill, 1.0, soft=1.4)
    elif ear == "nub":
        disc(arr, cx - 78, cy - 20, 22, fill, 1.0, soft=1.6)
        disc(arr, cx + 78, cy - 20, 22, fill, 1.0, soft=1.6)
    elif ear == "tri":
        ellipse(arr, cx - 62, cy - 86, 20, 34, fill, 1.0, soft=1.4)
        ellipse(arr, cx + 62, cy - 86, 20, 34, fill, 1.0, soft=1.4)
        ellipse(arr, cx - 62, cy - 80, 8, 16, rgb("ffb4c8"), 0.85, soft=1.1)
        ellipse(arr, cx + 62, cy - 80, 8, 16, rgb("ffb4c8"), 0.85, soft=1.1)
    elif ear == "horn":
        ellipse(arr, cx, cy - 108, 14, 36, fill, 1.0, soft=1.4)
        disc(arr, cx, cy - 136, 10, mix(fill, rgb("ffffff"), 0.2), 1.0, soft=1.2)
    # cheeks
    cheek = rgb("ff8fa3") if kind != "cat" else rgb("c45c7a")
    disc(arr, cx - 54, cy + 28, 12, cheek, 0.35, soft=3)
    disc(arr, cx + 54, cy + 28, 12, cheek, 0.35, soft=3)
    return arr


# --- faces ------------------------------------------------------------------

def paint_face(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    dy = bob(frame)
    cx, cy = HEAD[0], HEAD[1] + dy
    t = phase(frame)
    blink = 0.12 if (kind == "blink" and frame in (8, 9)) or (kind == "wink" and frame in (7, 8)) else 1.0
    left_open = 0.12 if kind == "wink" and frame in (7, 8) else blink
    right_open = blink if kind != "wink" else 1.0
    eye_c = rgb("1a1420")
    white = rgb("fffaf2")
    if kind == "sleepy":
        left_open = right_open = 0.38
    glow_amt = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t * 2)) if kind == "glow" else 1.0

    def eye(ex: float, open_amt: float, spark: bool = False) -> None:
        ellipse(arr, ex, cy - 6, 22, 20 * open_amt + 2, white, 0.98, soft=1.2)
        pupil_r = 9 if kind != "cross" else 0
        if kind == "cross":
            rect(arr, ex - 8, cy - 8, ex + 8, cy - 3, eye_c, 0.95, radius=2)
            rect(arr, ex - 2.4, cy - 16, ex + 2.4, cy + 4, eye_c, 0.95, radius=2)
        else:
            disc(arr, ex, cy - 4, pupil_r * open_amt + 1.5, eye_c, 0.96, soft=1.1)
            if kind == "glow":
                disc(arr, ex, cy - 4, 7, rgb("49f2c2"), 0.55 * glow_amt, soft=2)
            if spark:
                star(arr, ex + 1, cy - 6, 7, rgb("ffe38a"), 0.9, points=4)
            disc(arr, ex - 6, cy - 10, 3.4, white, 0.9, soft=0.8)

    spark = kind == "spark"
    eye(cx - 32, left_open, spark)
    eye(cx + 32, right_open, spark)
    if kind == "specs":
        # frames
        rect(arr, cx - 58, cy - 16, cx - 8, cy + 10, rgb("1a1420"), 0.0, radius=0)
        tmp = blank()
        # rims
        xx, yy = grid()
        for ex in (cx - 32, cx + 32):
            d = np.sqrt((xx - ex) ** 2 + (yy - (cy - 4)) ** 2)
            a = smoothstep(24, 21, d) * smoothstep(18, 21, d)
            tmp[..., :3] = rgb("2c2434")
            tmp[..., 3] = np.maximum(tmp[..., 3], a * 0.95)
        over(arr, tmp)
        rect(arr, cx - 10, cy - 6, cx + 10, cy - 2, rgb("2c2434"), 0.95, radius=2)
    # mouth
    if kind == "sleepy":
        ellipse(arr, cx, cy + 38, 10, 4, rgb("1a1420"), 0.7, soft=1)
    else:
        ellipse(arr, cx, cy + 40, 14, 7 + 1.5 * math.sin(t), rgb("1a1420"), 0.8, soft=1.1)
        ellipse(arr, cx, cy + 42, 10, 4, rgb("ff7a8a"), 0.35, soft=1.2)
    return arr


# --- wear -------------------------------------------------------------------

def paint_wear(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    dy = bob(frame)
    sway = math.sin(phase(frame) + 0.4) * 3
    cx, cy = HEAD[0] + sway * 0.15, HEAD[1] + dy
    if kind == "cap":
        ellipse(arr, cx, cy - 78, 78, 28, rgb("1f6b68"), 1.0, soft=1.6)
        rect(arr, cx - 4, cy - 108, cx + 56, cy - 88, rgb("1f6b68"), 1.0, radius=10)
        ellipse(arr, cx, cy - 96, 58, 26, rgb("2a8f8a"), 1.0, soft=1.4)
        disc(arr, cx, cy - 112, 8, rgb("49f2c2"), 1.0, soft=1.1)
    elif kind == "antenna":
        rect(arr, cx - 3, cy - 150, cx + 3, cy - 88, rgb("cfd6e4"), 0.95, radius=2)
        disc(arr, cx, cy - 156 + math.sin(phase(frame)) * 3, 11, rgb("ff5d8f"), 0.95, soft=1.2)
        glow(arr, cx, cy - 156, 18, rgb("ff5d8f"), 0.35)
    elif kind == "sprout":
        rect(arr, cx - 3, cy - 128, cx + 3, cy - 90, rgb("3d8b4a"), 0.95, radius=2)
        ellipse(arr, cx - 16, cy - 132 + math.sin(phase(frame)) * 2, 16, 10, rgb("7ed957"), 0.95, soft=1.2)
        ellipse(arr, cx + 16, cy - 128, 16, 10, rgb("7ed957"), 0.95, soft=1.2)
    elif kind == "crown":
        rect(arr, cx - 52, cy - 100, cx + 52, cy - 82, rgb("ffd36a"), 1.0, radius=6)
        for i, x in enumerate((-36, 0, 36)):
            disc(arr, cx + x, cy - 108 - (4 if i == 1 else 0), 10, rgb("ffe38a"), 1.0, soft=1.1)
        glow(arr, cx, cy - 100, 40, rgb("ffd36a"), 0.22 + 0.1 * math.sin(phase(frame)))
    elif kind == "hood":
        ellipse(arr, cx, cy - 20, 108, 100, rgb("3a2f6b"), 0.95, soft=2.2)
        ellipse(arr, cx, cy + 8, 78, 78, rgb("000000"), 0.0, soft=1)
        # opening
        xx, yy = grid()
        d = np.sqrt(((xx - cx) / 78) ** 2 + ((yy - (cy + 6)) / 78) ** 2)
        arr[..., 3] *= np.clip(1.0 - smoothstep(0.72, 0.92, d) + smoothstep(1.05, 0.98, d), 0, 1)
        # redraw hood rim only around head — simpler second pass
        hood = blank()
        ellipse(hood, cx, cy - 24, 110, 102, rgb("3a2f6b"), 1.0, soft=2)
        disc(hood, cx, cy + 10, 86, rgb("000000"), 1.0, soft=2)
        # keep pixels where hood exists and opening punched
        xx, yy = grid()
        opening = np.sqrt((xx - cx) ** 2 + (yy - (cy + 8)) ** 2) < 84
        hood[..., 3][opening] = 0
        # only keep upper hood
        hood[..., 3][yy > cy + 36] *= 0.15
        return hood
    elif kind == "halo":
        tmp = blank()
        glow(tmp, cx, cy - 108, 36, rgb("ffe38a"), 0.35 + 0.15 * math.sin(phase(frame)))
        xx, yy = grid()
        d = np.sqrt(((xx - cx) / 48) ** 2 + ((yy - (cy - 108)) / 16) ** 2)
        ring = smoothstep(1.18, 1.0, d) * smoothstep(0.72, 0.88, d)
        tmp[..., :3] = rgb("fff1c2")
        tmp[..., 3] = np.maximum(tmp[..., 3], ring * (0.85 + 0.1 * math.sin(phase(frame))))
        return tmp
    return arr


# --- charms -----------------------------------------------------------------

def paint_charm(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    t = phase(frame)
    cx, cy = HEAD
    if kind == "star":
        x = cx + math.cos(t) * 128
        y = cy - 10 + math.sin(t) * 46
        glow(arr, x, y, 22, rgb("ffe38a"), 0.45)
        star(arr, x, y, 16, rgb("ffd36a"), 0.96)
    elif kind == "heart":
        x = cx + 118
        y = cy + 8 + math.sin(t) * 10
        disc(arr, x - 7, y - 4, 9, rgb("ff5d8f"), 0.95, soft=1.2)
        disc(arr, x + 7, y - 4, 9, rgb("ff5d8f"), 0.95, soft=1.2)
        ellipse(arr, x, y + 8, 14, 12, rgb("ff5d8f"), 0.95, soft=1.2)
    elif kind == "bubble":
        x = cx - 120
        y = cy - 20 + math.sin(t) * 14
        disc(arr, x, y, 18, rgb("c8f4ff"), 0.35, soft=2)
        disc(arr, x - 5, y - 6, 5, rgb("ffffff"), 0.7, soft=1.2)
    elif kind == "leaf":
        x = cx + 110
        y = cy + 40 + math.sin(t) * 8
        ellipse(arr, x, y, 16, 9, rgb("7ed957"), 0.95, soft=1.2)
        rect(arr, x - 1, y - 12, x + 1, y, rgb("3d8b4a"), 0.9, radius=1)
    elif kind == "coin":
        x = cx - 112
        y = cy + 30 + math.sin(t) * 7
        squash = 14 + 6 * abs(math.cos(t))
        ellipse(arr, x, y, squash, 16, rgb("ffd36a"), 0.96, soft=1.2)
        ellipse(arr, x, y, squash * 0.55, 8, rgb("ffe38a"), 0.7, soft=1.1)
    elif kind == "spark":
        for i in range(5):
            a = t + i * 1.15
            x = cx + math.cos(a) * (100 + i * 8)
            y = cy + 20 + math.sin(a * 1.4) * (36 + i * 4)
            disc(arr, x, y, 3.2, rgb("c6f24a"), 0.7, soft=1.1)
    return arr


# --- catalog ----------------------------------------------------------------

TRAIT_SPEC = {
    "sky": [
        ("midnight", "Midnight Drift", 18),
        ("neon", "Neon Grid", 14),
        ("dawn", "Soft Dawn", 14),
        ("forest", "Firefly Grove", 12),
        ("coral", "Coral Dusk", 12),
        ("void", "Void Speckles", 12),
        ("candy", "Candy Wash", 10),
        ("storm", "Storm Flicker", 8),
    ],
    "aura": [
        ("none", "No aura", 22),
        ("mint", "Mint Pulse", 16),
        ("gold", "Gold Ring", 14),
        ("magenta", "Magenta Haze", 14),
        ("ice", "Ice Shimmer", 12),
        ("ember", "Ember Glow", 12),
        ("pixel", "Pixel Spark", 10),
    ],
    "body": [
        ("pudding", "Pudding", 22),
        ("fox", "Fox", 18),
        ("owl", "Owl", 16),
        ("frog", "Frog", 16),
        ("cat", "Cat", 16),
        ("beetle", "Beetle", 12),
    ],
    "face": [
        ("blink", "Blink", 24),
        ("sleepy", "Sleepy", 18),
        ("spark", "Spark", 16),
        ("wink", "Wink", 16),
        ("glow", "Glow", 14),
        ("specs", "Specs", 12),
    ],
    "wear": [
        ("none", "Bare head", 22),
        ("cap", "Mint Cap", 16),
        ("antenna", "Signal Antenna", 14),
        ("sprout", "Sprout", 14),
        ("crown", "Tiny Crown", 12),
        ("hood", "Night Hood", 12),
        ("halo", "Soft Halo", 10),
    ],
    "charm": [
        ("none", "None", 24),
        ("star", "Orbit Star", 16),
        ("heart", "Float Heart", 14),
        ("bubble", "Bubble", 14),
        ("leaf", "Leaf", 12),
        ("coin", "Spin Coin", 12),
        ("spark", "Spark Trail", 8),
    ],
}

PAINTERS = {
    "sky": SKIES,
    "aura": {k: (lambda kind: (lambda frame, k=kind: paint_aura(k, frame)))(k) for k in AURA_COLORS},
    "body": {k: (lambda kind: (lambda frame, k=kind: paint_body(k, frame)))(k) for k in BODIES},
    "face": {k: (lambda kind: (lambda frame, k=kind: paint_face(k, frame)))(k) for k in ("blink", "sleepy", "spark", "wink", "glow", "specs")},
    "wear": {k: (lambda kind: (lambda frame, k=kind: paint_wear(k, frame)))(k) for k in ("cap", "antenna", "sprout", "crown", "hood", "halo")},
    "charm": {k: (lambda kind: (lambda frame, k=kind: paint_charm(k, frame)))(k) for k in ("star", "heart", "bubble", "leaf", "coin", "spark")},
}

STACK = ("sky", "aura", "body", "face", "wear", "charm")

SIGNATURES = [
    {"sky": "midnight", "aura": "mint", "body": "pudding", "face": "blink", "wear": "cap", "charm": "star"},
    {"sky": "neon", "aura": "gold", "body": "fox", "face": "spark", "wear": "crown", "charm": "none"},
    {"sky": "dawn", "aura": "ice", "body": "owl", "face": "sleepy", "wear": "none", "charm": "bubble"},
    {"sky": "forest", "aura": "none", "body": "frog", "face": "wink", "wear": "sprout", "charm": "leaf"},
    {"sky": "void", "aura": "magenta", "body": "cat", "face": "glow", "wear": "hood", "charm": "spark"},
    {"sky": "storm", "aura": "ember", "body": "beetle", "face": "specs", "wear": "halo", "charm": "coin"},
    {"sky": "candy", "aura": "pixel", "body": "pudding", "face": "specs", "wear": "antenna", "charm": "heart"},
    {"sky": "coral", "aura": "gold", "body": "fox", "face": "blink", "wear": "cap", "charm": "none"},
    {"sky": "midnight", "aura": "ice", "body": "owl", "face": "glow", "wear": "halo", "charm": "star"},
    {"sky": "neon", "aura": "mint", "body": "frog", "face": "spark", "wear": "antenna", "charm": "none"},
    {"sky": "dawn", "aura": "none", "body": "cat", "face": "wink", "wear": "crown", "charm": "heart"},
    {"sky": "forest", "aura": "pixel", "body": "beetle", "face": "blink", "wear": "none", "charm": "leaf"},
    {"sky": "void", "aura": "gold", "body": "pudding", "face": "sleepy", "wear": "sprout", "charm": "coin"},
    {"sky": "storm", "aura": "magenta", "body": "fox", "face": "glow", "wear": "hood", "charm": "bubble"},
    {"sky": "candy", "aura": "ember", "body": "owl", "face": "specs", "wear": "cap", "charm": "spark"},
    {"sky": "coral", "aura": "mint", "body": "cat", "face": "spark", "wear": "antenna", "charm": "star"},
]


def trait_path(category: str, trait_id: str) -> Path:
    return TRAIT_DIR / category / f"{trait_id}.png"


def render_trait_frames(category: str, trait_id: str) -> list[Image.Image]:
    paint = PAINTERS[category][trait_id]
    return [to_image(paint(frame)) for frame in range(FRAMES)]


def compose_selection(selection: dict[str, str]) -> list[Image.Image]:
    layers: list[list[Image.Image]] = []
    for category in STACK:
        trait_id = selection[category]
        if trait_id == "none":
            continue
        path = trait_path(category, trait_id)
        if path.exists():
            with Image.open(path) as im:
                im.load()
                n = getattr(im, "n_frames", 1)
                frames = []
                for i in range(n):
                    im.seek(i)
                    frames.append(im.convert("RGBA").copy())
                layers.append(frames)
        else:
            layers.append(render_trait_frames(category, trait_id))
    out = []
    for i in range(FRAMES):
        canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        for frames in layers:
            canvas = Image.alpha_composite(canvas, frames[i % len(frames)])
        out.append(canvas)
    return out


def build_traits() -> None:
    TRAIT_DIR.mkdir(parents=True, exist_ok=True)
    for category, traits in TRAIT_SPEC.items():
        for trait_id, _name, _rarity in traits:
            if trait_id == "none":
                continue
            print(f"  {category}/{trait_id}")
            save_apng(render_trait_frames(category, trait_id), trait_path(category, trait_id))
    manifest = {
        "name": "Loopkins",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is an APNG. Studio stacks them live. Minted tokens flatten the same frame clock.",
    }
    (TRAIT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def name_of(category: str, trait_id: str) -> str:
    for item_id, name, _rarity in TRAIT_SPEC[category]:
        if item_id == trait_id:
            return name
    return trait_id


def build_samples() -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    META_DIR.mkdir(parents=True, exist_ok=True)
    samples = []
    for index, selection in enumerate(SIGNATURES, start=1):
        print(f"  sample #{index}")
        frames = compose_selection(selection)
        save_apng(frames, PREVIEW_DIR / f"{index}.png")
        samples.append(
            {
                "id": index,
                "name": f"Loopkin #{index}",
                "image": f"/generated-preview/{index}.png",
                "attributes": [
                    {"trait_type": label, "value": name_of(key, selection[key])}
                    for key, label in (
                        ("sky", "Sky"),
                        ("aura", "Aura"),
                        ("body", "Body"),
                        ("face", "Face"),
                        ("wear", "Wear"),
                        ("charm", "Charm"),
                    )
                ],
            }
        )
    (META_DIR / "samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")


def build_brand() -> None:
    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    logo_frames = compose_selection(SIGNATURES[0])
    # circular crop for logo
    logo = logo_frames[0].copy()
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse((24, 24, SIZE - 24, SIZE - 24), fill=255)
    logo.putalpha(Image.composite(logo.split()[-1], Image.new("L", (SIZE, SIZE), 0), mask))
    logo.save(BRAND_DIR / "logo-loopkins.png")
    save_apng(logo_frames, BRAND_DIR / "logo-loopkins-loop.png")

    banner = Image.new("RGBA", (1500, 560), (11, 16, 36, 255))
    # stitch three skies
    for i, sky_id in enumerate(("midnight", "neon", "coral")):
        sky = to_image(SKIES[sky_id](0)).resize((520, 520), Image.Resampling.LANCZOS)
        banner.alpha_composite(sky, (i * 490 - 20, 20))
    for i, sel in enumerate((SIGNATURES[0], SIGNATURES[1], SIGNATURES[4])):
        face = compose_selection(sel)[0].resize((340, 340), Image.Resampling.LANCZOS)
        banner.alpha_composite(face, (80 + i * 460, 150))
    draw = ImageDraw.Draw(banner)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 72)
        small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 28)
    except OSError:
        font = ImageFont.load_default()
        small = font
    draw.text((64, 36), "LOOPKINS", font=font, fill=(244, 241, 255, 255))
    draw.text((68, 112), "Layered APNG PFPs that never sit still.", font=small, fill=(201, 210, 230, 255))
    banner.convert("RGB").save(BRAND_DIR / "banner-loopkins.png", quality=94)
    ICON_PATH.parent.mkdir(parents=True, exist_ok=True)
    logo.resize((256, 256), Image.Resampling.LANCZOS).save(ICON_PATH)

    (META_DIR / "collection.json").write_text(
        json.dumps(
            {
                "name": "Loopkins",
                "description": "A 10,000-piece PFP collection of looping creatures assembled from layered APNG traits.",
                "image": "/brand/logo-loopkins.png",
                "banner_image": "/brand/banner-loopkins.png",
                "external_link": "/loopkins",
                "seller_fee_basis_points": 500,
                "fee_recipient": "0x0000000000000000000000000000000000000000",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    print("Building Loopkins APNG traits…")
    build_traits()
    print("Compositing sample tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
