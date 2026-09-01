#!/usr/bin/env python3
"""Paint Wicklings — looping paper-lantern PFP layers for an OpenSea Drop.

Every trait is a 12-frame APNG on a shared 512 canvas and 80ms clock, same as Loopkins.
Vessel, wick, and wrap share one hang (pendulum sway) so a stacked preview stays locked.
Night, halo, and drift move on their own loops.

Look: Loopkins-soft discs and glows. Translucent paper. A flame face that flickers.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gif_bake import save_loop_gif  # noqa: E402

TRAIT_DIR = ROOT / "public" / "wicklings-traits"
PREVIEW_DIR = ROOT / "public" / "wicklings-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"

SIZE = 512
FRAMES = 12
DURATION_MS = 80
H, W = SIZE, SIZE

HEAD = (256.0, 258.0)
HOOK = (256.0, 28.0)


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
    soft: float = 1.8,
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
    soft: float = 1.6,
) -> None:
    xx, yy = grid()
    d = np.sqrt(((xx - cx) / max(rx, 1.0)) ** 2 + ((yy - cy) / max(ry, 1.0)) ** 2)
    edge = soft / max(rx, ry, 1.0)
    a = smoothstep(1.0 + edge, 1.0 - edge, d) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def glow(dst: np.ndarray, cx: float, cy: float, r: float, color: np.ndarray, opacity: float) -> None:
    xx, yy = grid()
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = np.exp(-0.5 * (d / max(r, 1.0)) ** 2) * opacity
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


def rounded_rect(
    dst: np.ndarray,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    color: np.ndarray,
    opacity: float = 1.0,
    radius: float = 14.0,
    soft: float = 1.8,
) -> None:
    xx, yy = grid()
    ax = np.abs(xx - cx) - (rx - radius)
    ay = np.abs(yy - cy) - (ry - radius)
    d = np.sqrt(np.maximum(ax, 0.0) ** 2 + np.maximum(ay, 0.0) ** 2) + np.minimum(np.maximum(ax, ay), 0.0) - radius
    a = smoothstep(soft, -soft, d) * opacity
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


def write_bytes_retry(path: Path, data: bytes, attempts: int = 10) -> None:
    import time

    last_error: OSError | None = None
    for attempt in range(attempts):
        try:
            path.write_bytes(data)
            return
        except OSError as error:
            last_error = error
            time.sleep(0.15 * (attempt + 1))
    if last_error is not None:
        raise last_error


def save_image(image: Image.Image, path: Path, **kwargs) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fmt = kwargs.pop("format", None) or path.suffix.lstrip(".").upper()
    if fmt == "JPG":
        fmt = "JPEG"
    buffer = BytesIO()
    image.save(buffer, format=fmt, **kwargs)
    write_bytes_retry(path, buffer.getvalue())


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
        buffer := BytesIO(),
        save_all=True,
        append_images=stamped[1:],
        duration=[DURATION_MS] * len(stamped),
        loop=0,
        format="PNG",
        disposal=1,
        blend=0,
        compress_level=6,
    )
    write_bytes_retry(path, buffer.getvalue())


def phase(frame: int) -> float:
    return 2.0 * math.pi * frame / FRAMES


def hang(frame: int) -> tuple[float, float]:
    t = phase(frame)
    dx = math.sin(t) * 11.0
    dy = -abs(math.sin(t)) * 2.4
    return dx, dy


def flicker(frame: int) -> float:
    t = phase(frame)
    pop = 0.16 if frame in (2, 7) else (0.08 if frame in (3, 8) else 0.0)
    return 0.88 + 0.10 * math.sin(t * 2.15) + 0.07 * math.sin(t * 5.4 + 0.8) + pop


def seat(frame: int) -> tuple[float, float]:
    dx, dy = hang(frame)
    return HEAD[0] + dx, HEAD[1] + dy


# --- nights -----------------------------------------------------------------

def sky_wash(top: str, bot: str) -> np.ndarray:
    yy = grid()[1]
    arr = blank()
    arr[..., :3] = mix(rgb(top), rgb(bot), yy / SIZE)
    arr[..., 3] = 1.0
    return arr


def paint_night(kind: str, frame: int) -> np.ndarray:
    t = phase(frame)
    xx, yy = grid()

    if kind == "alley":
        arr = sky_wash("070814", "1a1428")
        rect(arr, 0, 0, 88, SIZE, rgb("0a0814"), 0.92)
        rect(arr, 424, 0, SIZE, SIZE, rgb("0c0a16"), 0.92)
        for i, (x, y) in enumerate(((28, 90), (28, 210), (28, 330), (456, 70), (456, 200), (456, 340))):
            pulse = 0.35 + 0.25 * (0.5 + 0.5 * math.sin(t + i * 0.9))
            rect(arr, x, y, x + 28, y + 38, rgb("ffc878"), pulse * 0.55, radius=3)
            glow(arr, x + 14, y + 18, 22, rgb("ffb14a"), pulse * 0.28)
        ellipse(arr, 256, 500, 240, 40, rgb("141018"), 0.55, soft=8)
        return arr

    if kind == "shrine":
        arr = sky_wash("1a1020", "3a2430")
        glow(arr, 256, 70, 160, rgb("ffd6a0"), 0.18 + 0.06 * math.sin(t))
        disc(arr, 390, 78, 42, rgb("fff1c8"), 0.9, soft=2.4)
        glow(arr, 390, 78, 70, rgb("ffe7a3"), 0.35)
        rect(arr, 118, 200, 142, 500, rgb("6b2430"), 0.92, radius=4)
        rect(arr, 370, 200, 394, 500, rgb("6b2430"), 0.92, radius=4)
        rect(arr, 108, 188, 404, 214, rgb("8a3040"), 0.95, radius=6)
        ellipse(arr, 256, 508, 220, 28, rgb("2a1c18"), 0.45, soft=6)
        rng = np.random.default_rng(7)
        for i in range(16):
            x = float(rng.uniform(40, 470))
            disc(arr, x, 478 + (i % 5), 2.2, rgb("c8b090"), 0.35, soft=1.1)
        return arr

    if kind == "rooftop":
        arr = sky_wash("0b1024", "1b2848")
        glow(arr, 256 + math.sin(t) * 12, 86, 150, rgb("6d8cff"), 0.16 + 0.05 * math.sin(t))
        rng = np.random.default_rng(11)
        for i in range(36):
            x = float(rng.uniform(16, 496))
            y = float(rng.uniform(16, 220))
            tw = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(t + i * 0.65))
            disc(arr, x, y, 1.1 + (i % 3) * 0.35, rgb("f4f1ff"), tw, soft=1.0)
        for i, (x, w, h) in enumerate(((40, 70, 160), (120, 90, 210), (230, 60, 140), (310, 110, 240), (430, 80, 180))):
            rect(arr, x, 520 - h, x + w, 520, rgb("070a16"), 0.88)
            if i % 2 == 0:
                glow(arr, x + w * 0.45, 500 - h * 0.35, 18, rgb("ffc878"), 0.22 + 0.1 * math.sin(t + i))
        return arr

    if kind == "festival":
        arr = sky_wash("2a1020", "4a2038")
        glow(arr, 256, 200, 220, rgb("ff8a5c"), 0.16 + 0.06 * math.sin(t))
        rng = np.random.default_rng(3)
        for i in range(14):
            x = 30 + i * 36 + math.sin(t + i) * 4
            y = 70 + (i % 3) * 28 + math.cos(t * 0.5 + i) * 3
            c = rgb("ffd36a") if i % 2 == 0 else rgb("ff8a6b")
            glow(arr, x, y, 14, c, 0.4)
            disc(arr, x, y, 7, c, 0.9, soft=1.2)
        rect(arr, 20, 58, 492, 64, rgb("4a2430"), 0.45, radius=2)
        return arr

    if kind == "fog":
        arr = sky_wash("1c2438", "4a5870")
        for i, (x, y, r) in enumerate(((90, 180, 110), (340, 140, 130), (200, 320, 150), (420, 360, 100))):
            glow(arr, x + math.sin(t + i) * 18, y + math.cos(t * 0.7 + i) * 10, r, rgb("d8e4f0"), 0.16 + 0.06 * math.sin(t + i))
        ellipse(arr, 256, 500, 260, 50, rgb("c8d4e4"), 0.22, soft=12)
        return arr

    if kind == "rain":
        arr = sky_wash("101428", "243050")
        flash = 0.22 if frame in (4, 9) else 0.0
        glow(arr, 280, 40, 180, rgb("d7c7ff"), 0.08 + flash)
        rng = np.random.default_rng(19)
        for i in range(48):
            x = (float(rng.uniform(8, 504)) + frame * (2.2 + i % 3)) % SIZE
            y = (float(rng.uniform(0, SIZE)) + frame * (14 + i % 5) * 1.6) % SIZE
            rect(arr, x, y, x + 1.4, y + 18, rgb("c8d8ff"), 0.18 + 0.1 * ((i + frame) % 4) / 4, radius=0)
        return arr

    if kind == "moon":
        arr = sky_wash("0b1024", "1a2448")
        moon_y = 118 + math.sin(t) * 4
        glow(arr, 360, moon_y, 110, rgb("fff1c2"), 0.42)
        disc(arr, 360, moon_y, 52, rgb("fff6d8"), 0.96, soft=2.4)
        disc(arr, 348, moon_y - 8, 16, rgb("efe0b8"), 0.35, soft=3)
        disc(arr, 378, moon_y + 12, 10, rgb("e8d4a8"), 0.28, soft=2)
        rng = np.random.default_rng(5)
        for i in range(28):
            x = float(rng.uniform(12, 500))
            y = float(rng.uniform(12, 260))
            tw = 0.25 + 0.75 * (0.5 + 0.5 * math.sin(t + i * 0.8))
            disc(arr, x, y, 1.15, rgb("f4f1ff"), tw, soft=0.9)
        ellipse(arr, 256, 508, 230, 26, rgb("0a1020"), 0.4, soft=8)
        return arr

    # ember
    arr = sky_wash("100808", "2a1410")
    glow(arr, 256, 420, 180, rgb("ff7a3d"), 0.14 + 0.08 * math.sin(t))
    rng = np.random.default_rng(21)
    for i in range(40):
        x = (float(rng.uniform(20, 490)) + math.cos(t + i) * 6) % SIZE
        y = (float(rng.uniform(40, 500)) - frame * (1.4 + i % 3) * 1.1) % SIZE
        c = rgb("ffd36a") if i % 3 else rgb("ff7a3d")
        glow(arr, x, y, 5, c, 0.28 + 0.4 * ((i + frame) % 5) / 5)
        disc(arr, x, y, 1.4, c, 0.7, soft=1.0)
    return arr


NIGHTS = ("alley", "shrine", "rooftop", "festival", "fog", "rain", "moon", "ember")


# --- halos ------------------------------------------------------------------

HALOS = ("gold", "mothdust", "firefly", "smoke", "heat")


def paint_halo(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    t = phase(frame)
    cx, cy = seat(frame)
    pulse = 0.30 + 0.16 * (0.5 + 0.5 * math.sin(t))
    if kind == "gold":
        glow(arr, cx, cy, 168 + 12 * math.sin(t), rgb("ffd36a"), pulse)
        glow(arr, cx, cy + 10, 96, rgb("ffe7a3"), pulse * 0.7)
        return arr
    if kind == "mothdust":
        glow(arr, cx, cy, 120, rgb("ffe7a3"), pulse * 0.45)
        rng = np.random.default_rng(9)
        for i in range(26):
            ang = t * 0.7 + i * 0.48
            x = cx + math.cos(ang) * (70 + (i % 5) * 14)
            y = cy + math.sin(ang * 1.1) * (50 + (i % 4) * 12)
            op = pulse * (0.35 + 0.65 * (0.5 + 0.5 * math.sin(t + i)))
            disc(arr, x, y, 1.6 + (i % 3) * 0.5, rgb("fff1c2"), op, soft=1.1)
        return arr
    if kind == "firefly":
        glow(arr, cx, cy, 130, rgb("d6ff7a"), pulse * 0.28)
        for i, radius in enumerate((88, 118, 148)):
            ang = t + i * 2.1
            x = cx + math.cos(ang) * radius
            y = cy + math.sin(ang) * radius * 0.62
            glow(arr, x, y, 10, rgb("d6ff7a"), 0.45 + 0.3 * math.sin(t * 2 + i))
            disc(arr, x, y, 2.4, rgb("f4ffc2"), 0.9, soft=1.0)
        return arr
    if kind == "smoke":
        for i in range(5):
            y = cy - 40 - i * 28 + math.sin(t + i) * 8
            x = cx + math.sin(t * 0.8 + i * 0.9) * (18 + i * 6)
            ellipse(arr, x, y, 22 + i * 8, 14 + i * 4, rgb("d8c8b8"), 0.10 + 0.04 * math.sin(t + i), soft=6)
        glow(arr, cx, cy, 100, rgb("c8b8a8"), pulse * 0.22)
        return arr
    # heat
    glow(arr, cx, cy, 150 + 18 * math.sin(t * 2), rgb("ff7a3d"), pulse * 0.55)
    glow(arr, cx, cy - 20, 70, rgb("ffd36a"), pulse * 0.4)
    for i in range(6):
        x = cx + math.sin(t * 1.4 + i) * (40 + i * 8)
        y = cy - 70 - i * 16 + math.cos(t + i) * 6
        ellipse(arr, x, y, 8, 18, rgb("ffb14a"), 0.08, soft=4)
    return arr


# --- vessels ----------------------------------------------------------------

VESSELS = {
    "round": {"paper": rgb("f3e0b8"), "shade": rgb("d4b888"), "trim": rgb("5a3a24"), "rx": 96.0, "ry": 102.0},
    "andon": {"paper": rgb("efe6d0"), "shade": rgb("c8b898"), "trim": rgb("2c2018"), "rx": 78.0, "ry": 118.0},
    "jar": {"paper": rgb("d4ece8"), "shade": rgb("8eb8b4"), "trim": rgb("c9a24a"), "rx": 72.0, "ry": 96.0},
    "teapot": {"paper": rgb("c5dcc8"), "shade": rgb("7aa080"), "trim": rgb("4a5c48"), "rx": 100.0, "ry": 86.0},
    "balloon": {"paper": rgb("f0b48a"), "shade": rgb("d48a62"), "trim": rgb("5a3020"), "rx": 88.0, "ry": 118.0},
    "temple": {"paper": rgb("c45c3a"), "shade": rgb("8a3424"), "trim": rgb("e8c878"), "rx": 84.0, "ry": 110.0},
}


def paper_body(arr: np.ndarray, cx: float, cy: float, rx: float, ry: float, paper: np.ndarray, shade_c: np.ndarray, box: bool) -> None:
    if box:
        rounded_rect(arr, cx, cy, rx, ry, shade_c, 1.0, radius=18, soft=2.0)
        rounded_rect(arr, cx, cy - 4, rx - 6, ry - 8, paper, 0.96, radius=16, soft=1.8)
    else:
        ellipse(arr, cx, cy + 6, rx, ry, shade_c, 1.0, soft=2.2)
        ellipse(arr, cx, cy, rx - 4, ry - 6, paper, 0.96, soft=2.0)
    xx, yy = grid()
    d = np.sqrt(((xx - cx) / max(rx * 0.72, 1)) ** 2 + ((yy - cy) / max(ry * 0.72, 1)) ** 2)
    window = np.clip(1.0 - d, 0.0, 1.0)
    window = window * window
    warm = mix(paper, rgb("ffe7a3"), 0.55)
    layer = blank()
    layer[..., :3] = warm
    layer[..., 3] = window * 0.42
    # keep punch inside the lantern
    inside = np.sqrt(((xx - cx) / max(rx - 2, 1)) ** 2 + ((yy - cy) / max(ry - 2, 1)) ** 2)
    layer[..., 3] *= smoothstep(1.02, 0.82, inside)
    over(arr, layer)
    # translucency: thin the center so halo reads through the paper ring
    punch = smoothstep(0.55, 0.08, d)
    mask = smoothstep(1.05, 0.88, inside)
    arr[..., 3] *= 1.0 - punch * mask * 0.38
    disc(arr, cx - rx * 0.28, cy - ry * 0.32, min(rx, ry) * 0.28, rgb("ffffff"), 0.18, soft=8)


def paint_vessel(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    spec = VESSELS[kind]
    dx, dy = hang(frame)
    cx, cy = HEAD[0] + dx, HEAD[1] + dy
    hx, hy = HOOK
    paper, shade_c, trim = spec["paper"], spec["shade"], spec["trim"]
    rx, ry = spec["rx"], spec["ry"]

    ellipse(arr, cx, 438 + dy * 0.2, 78, 14, rgb("000000"), 0.16, soft=7)

    # hanging cord
    rect(arr, hx - 2, hy, hx + 2, cy - ry + 8, rgb("c8b090"), 0.95, radius=2)
    disc(arr, hx, hy, 5, trim, 1.0, soft=1.1)

    if kind == "round":
        paper_body(arr, cx, cy, rx, ry, paper, shade_c, box=False)
        ellipse(arr, cx, cy - ry + 8, 42, 12, trim, 1.0, soft=1.4)
        ellipse(arr, cx, cy + ry - 10, 48, 14, trim, 1.0, soft=1.4)
        disc(arr, cx, cy - ry - 4, 7, trim, 1.0, soft=1.1)
    elif kind == "andon":
        paper_body(arr, cx, cy, rx, ry, paper, shade_c, box=True)
        rounded_rect(arr, cx, cy - ry + 6, rx + 4, 12, trim, 1.0, radius=4, soft=1.2)
        rounded_rect(arr, cx, cy + ry - 8, rx + 4, 12, trim, 1.0, radius=4, soft=1.2)
        rect(arr, cx - rx + 10, cy - ry + 16, cx - rx + 16, cy + ry - 16, trim, 0.55, radius=2)
        rect(arr, cx + rx - 16, cy - ry + 16, cx + rx - 10, cy + ry - 16, trim, 0.55, radius=2)
    elif kind == "jar":
        paper_body(arr, cx, cy + 8, rx, ry, paper, shade_c, box=False)
        disc(arr, cx - rx * 0.3, cy - 10, 22, rgb("ffffff"), 0.22, soft=6)
        rounded_rect(arr, cx, cy - ry + 4, 48, 16, trim, 1.0, radius=6, soft=1.3)
        rounded_rect(arr, cx, cy - ry - 10, 36, 10, mix(trim, rgb("ffffff"), 0.25), 1.0, radius=4, soft=1.2)
        ellipse(arr, cx, cy + ry - 4, 40, 10, mix(shade_c, rgb("ffffff"), 0.15), 0.5, soft=2)
    elif kind == "teapot":
        paper_body(arr, cx, cy + 6, rx, ry, paper, shade_c, box=False)
        ellipse(arr, cx + rx + 8, cy + 8, 28, 16, shade_c, 1.0, soft=1.6)
        ellipse(arr, cx + rx + 22, cy + 4, 18, 22, paper, 1.0, soft=1.5)
        # handle
        tmp = blank()
        ellipse(tmp, cx - rx - 6, cy, 22, 34, trim, 0.95, soft=1.6)
        ellipse(tmp, cx - rx - 4, cy, 12, 22, rgb("000000"), 1.0, soft=1.4)
        xx, yy = grid()
        hole = np.sqrt(((xx - (cx - rx - 4)) / 12) ** 2 + ((yy - cy) / 22) ** 2) < 1.0
        tmp[..., 3][hole] = 0
        over(arr, tmp)
        ellipse(arr, cx, cy - ry + 6, 28, 12, trim, 1.0, soft=1.3)
    elif kind == "balloon":
        paper_body(arr, cx, cy - 8, rx, ry, paper, shade_c, box=False)
        ellipse(arr, cx, cy + ry - 18, 22, 16, shade_c, 1.0, soft=1.5)
        rounded_rect(arr, cx, cy + ry + 10, 28, 16, trim, 1.0, radius=5, soft=1.3)
        rect(arr, cx - 14, cy + ry - 8, cx - 11, cy + ry + 6, trim, 0.9, radius=1)
        rect(arr, cx + 11, cy + ry - 8, cx + 14, cy + ry + 6, trim, 0.9, radius=1)
        disc(arr, cx, cy - ry - 6, 8, trim, 1.0, soft=1.1)
    else:
        # temple
        paper_body(arr, cx, cy + 8, rx, ry, paper, shade_c, box=True)
        # roof
        ellipse(arr, cx, cy - ry + 4, rx + 18, 22, trim, 1.0, soft=1.6)
        ellipse(arr, cx, cy - ry - 10, 36, 14, mix(trim, rgb("ffffff"), 0.2), 1.0, soft=1.4)
        disc(arr, cx, cy - ry - 22, 8, trim, 1.0, soft=1.1)
        rounded_rect(arr, cx, cy + ry - 6, rx + 6, 12, trim, 1.0, radius=4, soft=1.2)

    return arr


# --- wick (flame + face) ----------------------------------------------------

def paint_wick(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = seat(frame)
    t = phase(frame)
    fl = flicker(frame)
    flame_h = 54 * fl
    flame_w = 38 + 4 * math.sin(t * 3)

    glow(arr, cx, cy + 6, 70 * fl, rgb("ffd36a"), 0.42 + 0.18 * (fl - 0.88))
    ellipse(arr, cx, cy + 10, flame_w + 8, flame_h + 10, rgb("ff7a3d"), 0.55, soft=4)
    ellipse(arr, cx, cy + 4, flame_w, flame_h, rgb("ffb14a"), 0.92, soft=2.4)
    ellipse(arr, cx, cy + 12, flame_w * 0.62, flame_h * 0.62, rgb("ffe7a3"), 0.95, soft=2.0)
    ellipse(arr, cx, cy + 18, flame_w * 0.32, flame_h * 0.34, rgb("fffaf0"), 0.9, soft=1.8)

    blink = 0.14 if (kind == "blink" and frame in (8, 9)) or (kind == "wink" and frame in (7, 8)) else 1.0
    left_open = 0.14 if kind == "wink" and frame in (7, 8) else blink
    right_open = blink if kind != "wink" else 1.0
    if kind == "sleepy":
        left_open = right_open = 0.36
    if kind == "wide":
        left_open = right_open = 1.15

    eye_c = rgb("1a1420")
    white = rgb("fffaf2")
    face_y = cy + 8

    def eye(ex: float, open_amt: float, spark: bool = False) -> None:
        oh = max(open_amt, 0.12)
        ellipse(arr, ex, face_y - 6, 15, 13 * oh + 1.5, white, 0.98, soft=1.1)
        disc(arr, ex, face_y - 4, 6.5 * min(oh, 1.0) + 1.2, eye_c, 0.96, soft=1.0)
        if kind == "spark" or spark:
            star(arr, ex + 1, face_y - 6, 5.5, rgb("ffe38a"), 0.85, points=4)
        disc(arr, ex - 4, face_y - 9, 2.4, white, 0.9, soft=0.7)

    spark = kind == "spark"
    eye(cx - 22, left_open, spark)
    eye(cx + 22, right_open, spark)

    disc(arr, cx - 34, face_y + 16, 9, rgb("ff8fa3"), 0.38, soft=3)
    disc(arr, cx + 34, face_y + 16, 9, rgb("ff8fa3"), 0.38, soft=3)

    if kind == "grin":
        ellipse(arr, cx, face_y + 28, 16, 7 + 1.2 * math.sin(t), rgb("1a1420"), 0.85, soft=1.1)
        ellipse(arr, cx, face_y + 30, 11, 4, rgb("ff7a8a"), 0.4, soft=1.1)
    elif kind == "sleepy":
        ellipse(arr, cx, face_y + 26, 9, 3.5, rgb("1a1420"), 0.7, soft=1.0)
    elif kind == "wide":
        ellipse(arr, cx, face_y + 30, 8, 8 + 1.5 * math.sin(t), rgb("1a1420"), 0.85, soft=1.1)
        ellipse(arr, cx, face_y + 32, 5, 4, rgb("ff7a8a"), 0.35, soft=1.0)
    else:
        ellipse(arr, cx, face_y + 28, 12, 6 + 1.4 * math.sin(t), rgb("1a1420"), 0.8, soft=1.1)
        ellipse(arr, cx, face_y + 30, 8, 3.5, rgb("ff7a8a"), 0.32, soft=1.1)

    # wick stub under the flame
    rect(arr, cx - 3, cy + flame_h * 0.55, cx + 3, cy + flame_h * 0.55 + 16, rgb("5a3a24"), 0.85, radius=2)
    return arr


WICKS = ("blink", "sleepy", "spark", "grin", "wink", "wide")


# --- wrap -------------------------------------------------------------------

WRAPS = ("stripe", "floral", "twine", "stamp", "cracks", "tarot")


def paint_wrap(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = seat(frame)
    t = phase(frame)
    dx, dy = hang(frame)

    if kind == "stripe":
        for i, yoff in enumerate((-48, -8, 32, 70)):
            c = rgb("c45c3a") if i % 2 == 0 else rgb("5a3a24")
            ellipse(arr, cx, cy + yoff, 78, 7, c, 0.55, soft=1.6)
        return arr
    if kind == "floral":
        rng = np.random.default_rng(14)
        for i in range(9):
            ang = i * 0.7 + 0.4
            x = cx + math.cos(ang) * 72
            y = cy + math.sin(ang) * 78
            petal = rgb("ff8fa3") if i % 2 == 0 else rgb("ffe38a")
            disc(arr, x, y, 8, petal, 0.8, soft=1.4)
            disc(arr, x, y, 3.2, rgb("fff1c2"), 0.9, soft=1.0)
        return arr
    if kind == "twine":
        ellipse(arr, cx, cy + 86, 70, 10, rgb("8a6240"), 0.85, soft=1.5)
        ellipse(arr, cx, cy + 92, 62, 7, rgb("c8a070"), 0.7, soft=1.3)
        lag = math.sin(t + 0.7) * 8
        tx, ty = cx + lag, cy + 128 + abs(math.sin(t + 0.7)) * 4
        ellipse(arr, tx, ty, 10, 22, rgb("c45c3a"), 0.95, soft=1.4)
        ellipse(arr, tx, ty + 4, 6, 14, rgb("ffd36a"), 0.7, soft=1.2)
        rect(arr, cx - 2, cy + 96, cx + 2, ty - 16, rgb("8a6240"), 0.9, radius=1)
        return arr
    if kind == "stamp":
        sx, sy = cx + 58, cy - 20
        rounded_rect(arr, sx, sy, 22, 24, rgb("8a2430"), 0.88, radius=4, soft=1.2)
        disc(arr, sx, sy, 10, rgb("c45c3a"), 0.0, soft=1)
        star(arr, sx, sy, 9, rgb("ffd36a"), 0.9, points=5)
        return arr
    if kind == "cracks":
        for i, (x0, y0, x1, y1) in enumerate(
            (
                (cx - 40, cy - 50, cx - 8, cy - 10),
                (cx + 20, cy - 60, cx + 48, cy - 18),
                (cx - 30, cy + 20, cx + 10, cy + 70),
                (cx + 36, cy + 8, cx + 60, cy + 50),
            )
        ):
            rect(arr, min(x0, x1), min(y0, y1), min(x0, x1) + 2.2, max(y0, y1), rgb("3a2418"), 0.55, radius=1)
        return arr
    # tarot
    star(arr, cx, cy - 78, 16, rgb("ffe38a"), 0.85 + 0.1 * math.sin(t), points=4)
    glow(arr, cx, cy - 78, 22, rgb("ffd36a"), 0.28)
    disc(arr, cx + 62, cy + 8, 16, rgb("e8d4a8"), 0.55, soft=2)
    disc(arr, cx + 58, cy + 6, 10, rgb("fff1c2"), 0.4, soft=2)
    return arr


# --- drift ------------------------------------------------------------------

DRIFTS = ("moth", "spark", "incense", "petal", "wax")


def paint_drift(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    t = phase(frame)
    cx, cy = HEAD

    if kind == "moth":
        ang = t
        mx = cx + math.cos(ang) * 132
        my = cy - 8 + math.sin(ang) * 48
        flap = 10 + 16 * abs(math.sin(t * 2))
        wing = rgb("efe0c4")
        ellipse(arr, mx - flap * 0.55, my, 16, 8, wing, 0.78, soft=1.4)
        ellipse(arr, mx + flap * 0.55, my, 16, 8, wing, 0.78, soft=1.4)
        ellipse(arr, mx, my, 8, 6, rgb("5a3a24"), 0.95, soft=1.2)
        disc(arr, mx - 3, my - 2, 1.6, rgb("1a1420"), 0.9, soft=0.7)
        disc(arr, mx + 3, my - 2, 1.6, rgb("1a1420"), 0.9, soft=0.7)
        glow(arr, mx, my, 16, rgb("ffe7a3"), 0.22)
        return arr
    if kind == "spark":
        rng = np.random.default_rng(12)
        for i in range(18):
            x = cx + float(rng.uniform(-90, 90))
            y = (cy + 40 + float(rng.uniform(-80, 80)) - frame * (3 + i % 4) * 2.2) % SIZE
            c = rgb("ffd36a") if i % 2 else rgb("fff1c2")
            glow(arr, x, y, 7, c, 0.35 + 0.3 * math.sin(t + i))
            disc(arr, x, y, 1.8, c, 0.85, soft=0.9)
        return arr
    if kind == "incense":
        for i in range(7):
            y = cy - 30 - i * 22 + math.sin(t + i * 0.6) * 6
            x = cx + 70 + math.sin(t * 0.9 + i * 0.8) * (10 + i * 5)
            ellipse(arr, x, y, 10 + i * 3, 16 + i * 2, rgb("d8c8e8"), 0.10 + 0.04 * (1 - i / 7), soft=5)
        rect(arr, cx + 68, cy + 70, cx + 74, cy + 118, rgb("5a3a24"), 0.9, radius=2)
        disc(arr, cx + 71, cy + 68, 4, rgb("ff7a3d"), 0.8, soft=1.2)
        return arr
    if kind == "petal":
        rng = np.random.default_rng(4)
        for i in range(10):
            x = (40 + i * 46 + math.sin(t + i) * 18) % SIZE
            y = (float(rng.uniform(20, 480)) + frame * (2.5 + i % 3)) % SIZE
            rot = 8 + 4 * math.sin(t + i)
            c = rgb("ff8fa3") if i % 2 else rgb("ffe0ea")
            ellipse(arr, x, y, rot, 5, c, 0.8, soft=1.3)
        return arr
    # wax
    dx, dy = hang(frame)
    lx, ly = HEAD[0] + dx, HEAD[1] + dy + 96
    drip = 18 + 10 * (0.5 + 0.5 * math.sin(t))
    ellipse(arr, lx, ly, 16, 8, rgb("fff1c2"), 0.9, soft=1.4)
    ellipse(arr, lx, ly + drip * 0.45, 7, drip, rgb("ffe7a3"), 0.88, soft=1.5)
    disc(arr, lx, ly + drip, 6, rgb("ffd36a"), 0.9, soft=1.2)
    return arr


# --- catalog ----------------------------------------------------------------

TRAIT_SPEC = {
    "night": [
        ("alley", "Lantern Alley", 16),
        ("shrine", "Shrine Path", 14),
        ("rooftop", "Rooftop Night", 14),
        ("festival", "Festival Street", 12),
        ("fog", "Soft Fog", 12),
        ("moon", "Full Moon", 12),
        ("rain", "Paper Rain", 10),
        ("ember", "Ember Void", 10),
    ],
    "halo": [
        ("none", "No halo", 22),
        ("gold", "Gold Bloom", 16),
        ("mothdust", "Moth Dust", 14),
        ("firefly", "Firefly Ring", 14),
        ("smoke", "Incense Smoke", 12),
        ("heat", "Heat Shimmer", 12),
    ],
    "vessel": [
        ("round", "Round Paper", 20),
        ("andon", "Andon", 18),
        ("jar", "Glow Jar", 16),
        ("teapot", "Teapot", 16),
        ("balloon", "Sky Lantern", 16),
        ("temple", "Temple Hang", 14),
    ],
    "wick": [
        ("blink", "Blink", 22),
        ("sleepy", "Sleepy", 18),
        ("spark", "Spark", 16),
        ("grin", "Grin", 16),
        ("wink", "Wink", 14),
        ("wide", "Wide", 14),
    ],
    "wrap": [
        ("none", "Bare paper", 22),
        ("stripe", "Ink Stripe", 16),
        ("floral", "Floral", 14),
        ("twine", "Twine Tassel", 14),
        ("stamp", "Red Stamp", 12),
        ("cracks", "Hairline Cracks", 12),
        ("tarot", "Moon Tarot", 10),
    ],
    "drift": [
        ("none", "None", 22),
        ("moth", "Orbit Moth", 16),
        ("spark", "Spark Trail", 14),
        ("incense", "Incense Curl", 14),
        ("petal", "Falling Petal", 12),
        ("wax", "Wax Drip", 10),
    ],
}

PAINTERS = {
    "night": {k: (lambda kind: (lambda frame, k=kind: paint_night(k, frame)))(k) for k in NIGHTS},
    "halo": {k: (lambda kind: (lambda frame, k=kind: paint_halo(k, frame)))(k) for k in HALOS},
    "vessel": {k: (lambda kind: (lambda frame, k=kind: paint_vessel(k, frame)))(k) for k in VESSELS},
    "wick": {k: (lambda kind: (lambda frame, k=kind: paint_wick(k, frame)))(k) for k in WICKS},
    "wrap": {k: (lambda kind: (lambda frame, k=kind: paint_wrap(k, frame)))(k) for k in WRAPS},
    "drift": {k: (lambda kind: (lambda frame, k=kind: paint_drift(k, frame)))(k) for k in DRIFTS},
}

STACK = ("night", "halo", "vessel", "wick", "wrap", "drift")

SIGNATURES = [
    {"night": "alley", "halo": "gold", "vessel": "round", "wick": "blink", "wrap": "twine", "drift": "moth"},
    {"night": "festival", "halo": "heat", "vessel": "temple", "wick": "grin", "wrap": "stamp", "drift": "petal"},
    {"night": "moon", "halo": "mothdust", "vessel": "andon", "wick": "sleepy", "wrap": "stripe", "drift": "none"},
    {"night": "shrine", "halo": "firefly", "vessel": "teapot", "wick": "wink", "wrap": "floral", "drift": "incense"},
    {"night": "rooftop", "halo": "none", "vessel": "balloon", "wick": "spark", "wrap": "tarot", "drift": "spark"},
    {"night": "ember", "halo": "heat", "vessel": "jar", "wick": "wide", "wrap": "none", "drift": "wax"},
    {"night": "fog", "halo": "smoke", "vessel": "round", "wick": "blink", "wrap": "cracks", "drift": "moth"},
    {"night": "rain", "halo": "gold", "vessel": "andon", "wick": "grin", "wrap": "twine", "drift": "petal"},
    {"night": "alley", "halo": "firefly", "vessel": "temple", "wick": "spark", "wrap": "floral", "drift": "none"},
    {"night": "festival", "halo": "mothdust", "vessel": "balloon", "wick": "wink", "wrap": "stripe", "drift": "spark"},
    {"night": "moon", "halo": "none", "vessel": "teapot", "wick": "sleepy", "wrap": "stamp", "drift": "incense"},
    {"night": "shrine", "halo": "gold", "vessel": "jar", "wick": "blink", "wrap": "tarot", "drift": "wax"},
    {"night": "rooftop", "halo": "smoke", "vessel": "round", "wick": "wide", "wrap": "none", "drift": "moth"},
    {"night": "ember", "halo": "heat", "vessel": "temple", "wick": "grin", "wrap": "cracks", "drift": "spark"},
    {"night": "fog", "halo": "firefly", "vessel": "andon", "wick": "spark", "wrap": "twine", "drift": "none"},
    {"night": "rain", "halo": "mothdust", "vessel": "balloon", "wick": "wink", "wrap": "floral", "drift": "petal"},
]

TRAIT_LABELS = (
    ("night", "Night"),
    ("halo", "Halo"),
    ("vessel", "Vessel"),
    ("wick", "Wick"),
    ("wrap", "Wrap"),
    ("drift", "Drift"),
)


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


def name_of(category: str, trait_id: str) -> str:
    for item_id, name, _rarity in TRAIT_SPEC[category]:
        if item_id == trait_id:
            return name
    return trait_id


def build_traits() -> None:
    TRAIT_DIR.mkdir(parents=True, exist_ok=True)
    for category, traits in TRAIT_SPEC.items():
        for trait_id, _name, _rarity in traits:
            if trait_id == "none":
                continue
            print(f"  {category}/{trait_id}")
            save_apng(render_trait_frames(category, trait_id), trait_path(category, trait_id))
    manifest = {
        "name": "Wicklings",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF.",
    }
    (TRAIT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def build_samples() -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    META_DIR.mkdir(parents=True, exist_ok=True)
    samples = []
    for index, selection in enumerate(SIGNATURES, start=1):
        print(f"  sample #{index}")
        frames = compose_selection(selection)
        save_loop_gif(frames, PREVIEW_DIR / f"{index}.gif", DURATION_MS)
        samples.append(
            {
                "id": index,
                "name": f"Wickling #{index}",
                "image": f"/wicklings-preview/{index}.gif",
                "attributes": [{"trait_type": label, "value": name_of(key, selection[key])} for key, label in TRAIT_LABELS],
            }
        )
    (META_DIR / "wicklings-samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")


COLLECTION_DESCRIPTION = (
    "Wicklings is a 10,000-piece collection of looping paper-lantern PFP GIFs on Arbitrum. "
    "Each one is a little flame living in a paper house — stacked from night, halo, vessel, wick, wrap, and drift, "
    "then flattened onto one 12-frame GIF. The lantern sways. The wick blinks. Moths never land."
)

COLLECTION_STORY = (
    "Wicklings never go out.\n\n"
    "A 10,000-piece collection of looping paper-lantern PFP GIFs on Arbitrum. "
    "Each Wickling is a little flame that moved into a paper house. The lantern sways. "
    "The wick is the face — it blinks, it flickers, it never cools. Nights hang behind them. "
    "Halos breathe. Moths orbit and never land.\n\n"
    "Six layers on one 12-frame clock: night, halo, vessel, wick, wrap, and drift. "
    "Soft discs. Translucent paper. Warm amber on night indigo.\n\n"
    "Minting on Arbitrum (chain ID 42161). Gas is ETH."
)


def panoramic_wash(width: int, height: int, frame: int = 0) -> Image.Image:
    left = np.asarray(to_image(paint_night("alley", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    mid = np.asarray(to_image(paint_night("festival", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    right = np.asarray(to_image(paint_night("moon", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)[None, :, None]
    w_left = np.clip(1.0 - x / 0.42, 0.0, 1.0)
    w_right = np.clip((x - 0.58) / 0.42, 0.0, 1.0)
    w_mid = np.clip(1.0 - w_left - w_right, 0.0, 1.0)
    out = left * w_left + mid * w_mid + right * w_right
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")


def rounded_portrait(portrait: Image.Image, size: int, radius: int = 56) -> Image.Image:
    face = portrait.resize((size, size), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    face.putalpha(Image.composite(face.split()[-1], Image.new("L", (size, size), 0), mask))
    return face


def place_portrait(canvas: Image.Image, portrait: Image.Image, x: int, y: int, size: int, radius: int = 56) -> None:
    face = rounded_portrait(portrait, size, radius)
    shadow = Image.new("RGBA", (size + 24, size + 24), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((8, 14, size + 8, size + 18), radius=radius, fill=(8, 8, 20, 90))
    canvas.alpha_composite(shadow, (x - 8, y - 6))
    canvas.alpha_composite(face, (x, y))


def lineup_banner(width: int, height: int, portraits: list[Image.Image]) -> Image.Image:
    canvas = panoramic_wash(width, height, frame=4)
    count = len(portraits)
    size = int(height * 0.82)
    overlap = size // 5
    total = size * count - overlap * (count - 1)
    start_x = (width - total) // 2
    y = (height - size) // 2 + int(height * 0.04)
    for index, portrait in enumerate(portraits):
        x = start_x + index * (size - overlap)
        place_portrait(canvas, portrait, x, y, size, radius=max(36, size // 10))
    return canvas


def write_collection_meta() -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    (META_DIR / "wicklings-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "wicklings.json").write_text(
        json.dumps(
            {
                "name": "Wicklings",
                "symbol": "WICK",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-wicklings.gif",
                "featured_image": "/brand/featured-wicklings.jpg",
                "banner_image": "/brand/banner-wicklings.png",
                "opensea_banner_image": "/brand/banner-wicklings-opensea.jpg",
                "external_link": "/wicklings",
                "seller_fee_basis_points": 500,
                "fee_recipient": "0x0000000000000000000000000000000000000000",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def build_brand() -> None:
    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    portraits = [compose_selection(selection)[0] for selection in SIGNATURES[:7]]
    logo_frames = compose_selection(SIGNATURES[0])

    logo = logo_frames[0].copy()
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse((18, 18, SIZE - 18, SIZE - 18), fill=255)
    logo.putalpha(Image.composite(logo.split()[-1], Image.new("L", (SIZE, SIZE), 0), mask))
    ring = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((10, 10, SIZE - 10, SIZE - 10), outline=(255, 211, 106, 220), width=10)
    logo = Image.alpha_composite(logo, ring)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-wicklings.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-wicklings-loop.png",
    )

    site_banner = lineup_banner(1500, 560, portraits[:5])
    save_image(site_banner.convert("RGB"), BRAND_DIR / "banner-wicklings.png", quality=94)

    opensea_banner = lineup_banner(2800, 700, portraits)
    save_image(opensea_banner.convert("RGB"), BRAND_DIR / "banner-wicklings-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800, frame=8)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=64)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=64)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-wicklings.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(gif_frames, BRAND_DIR / "collection-wicklings.gif", DURATION_MS)
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true", help="Rebuild logo, banners, and listing copy")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Wicklings brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Wicklings trait loops…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
