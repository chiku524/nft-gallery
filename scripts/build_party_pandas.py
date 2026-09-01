#!/usr/bin/env python3
"""Paint Party Pandas — looping party-panda PFP layers for an OpenSea Drop on Base.

Every trait is a 12-frame APNG on a shared 512 canvas and 80ms clock, same as Loopkins.
Panda, mood, fit, and extra share one bob so a stacked preview stays locked together.
Venue and glow move on their own loops. Soft edges only — no pixel art.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gif_bake import save_loop_gif  # noqa: E402

TRAIT_DIR = ROOT / "public" / "party-pandas-traits"
PREVIEW_DIR = ROOT / "public" / "party-pandas-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"

SIZE = 512
FRAMES = 12
DURATION_MS = 80
H, W = SIZE, SIZE

HEAD = (256.0, 236.0)


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
    soft: float = 10.0,
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
    soft: float = 10.0,
) -> None:
    xx, yy = grid()
    d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    edge = soft / max(rx, ry)
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


def grain(seed: int, amp: float = 0.04) -> np.ndarray:
    rng = np.random.default_rng(seed)
    small = (rng.random((SIZE // 16, SIZE // 16)) * 2 - 1).astype(np.float32)
    im = Image.fromarray(((small + 1) * 127.5).astype(np.uint8), "L")
    big = np.asarray(im.resize((W, H), Image.Resampling.BICUBIC), dtype=np.float32) / 127.5 - 1.0
    return big * amp


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
        compress_level=6,
    )


def bob(frame: int, amp: float = 5.0) -> float:
    return math.sin(2 * math.pi * frame / FRAMES) * amp


def phase(frame: int) -> float:
    return 2.0 * math.pi * frame / FRAMES


def blink_amount(frame: int, closed_at: int = 8) -> float:
    dist = min(abs(frame - closed_at), abs(frame - closed_at + FRAMES), abs(frame - closed_at - FRAMES))
    if dist == 0:
        return 1.0
    if dist == 1:
        return 0.55
    return 0.0


# --- venue ------------------------------------------------------------------

VENUES = {
    "disco": ("120818", "3a1048", "e040a0", 7),
    "neon": ("061018", "083848", "20e0d0", 11),
    "bamboo": ("102018", "2a5040", "80c878", 13),
    "rooftop": ("0c1028", "243060", "f0c070", 17),
    "candy": ("281018", "803060", "f090c8", 19),
    "moonlight": ("101428", "283868", "c8d8f0", 23),
    "confetti": ("241810", "704028", "f0c060", 29),
    "garden": ("182018", "406040", "f0a0b0", 31),
}


def paint_venue(kind: str, frame: int) -> np.ndarray:
    top_h, mid_h, bot_h, seed = VENUES[kind]
    xx, yy = grid()
    t = phase(frame)
    top, mid, bot = rgb(top_h), rgb(mid_h), rgb(bot_h)
    v = yy / (H - 1)
    low = mix(top, mid, v / 0.52)
    high = mix(mid, bot, (v - 0.52) / 0.48)
    wash = np.where((v < 0.52)[..., None], low, high)
    arr = blank()
    arr[..., :3] = wash
    arr[..., 3] = 1.0
    texture = grain(seed, 0.045)
    arr[..., :3] = np.clip(arr[..., :3] + texture[..., None], 0.0, 1.0)

    if kind == "disco":
        for i, color in enumerate((rgb("ff40c0"), rgb("40e0ff"), rgb("ffe040"))):
            ang = t + i * 2.1
            glow(arr, 256 + math.cos(ang) * 140, 160 + math.sin(ang * 1.3) * 70, 90, color, 0.22)
        glow(arr, 256, 420, 160, bot, 0.18)
    elif kind == "neon":
        for i in range(5):
            gy = 70 + i * 80 + math.sin(t + i) * 8
            ellipse(arr, 256, gy, 280, 6, bot, 0.16 + 0.04 * math.sin(t + i), soft=8)
        glow(arr, 80 + math.sin(t) * 20, 180, 70, rgb("20e0d0"), 0.2)
        glow(arr, 430, 320 + math.cos(t) * 16, 80, rgb("ff40c0"), 0.16)
    elif kind == "bamboo":
        stem = rgb("2a5040")
        for i, x in enumerate((70, 150, 380, 460)):
            sway = math.sin(t + i) * 6
            ellipse(arr, x + sway, 260, 14, 280, stem, 0.55, soft=12)
            disc(arr, x + sway + 10, 90 + (i % 3) * 40, 22, bot, 0.28, soft=10)
        glow(arr, 256, 200, 180, bot, 0.12)
    elif kind == "rooftop":
        glow(arr, 400, 90, 50, bot, 0.35 + 0.08 * math.sin(t))
        for i, (bx, bh) in enumerate(((40, 160), (90, 220), (150, 140), (360, 180), (430, 240), (480, 150))):
            ellipse(arr, bx, 430, 28, bh, top, 0.7, soft=8)
        glow(arr, 120, 380, 80, mid, 0.12)
    elif kind == "candy":
        glow(arr, 140 + math.sin(t) * 30, 140, 140, bot, 0.22)
        glow(arr, 380, 300 + math.cos(t) * 20, 120, rgb("80e0ff"), 0.14)
        glow(arr, 256, 420, 160, mid, 0.16)
    elif kind == "moonlight":
        glow(arr, 380, 90, 70, bot, 0.4 + 0.08 * math.sin(t))
        glow(arr, 380, 90, 140, mid, 0.16)
        for i in range(18):
            px = (37 * i + frame * 11) % W
            py = (73 * i + 40) % 220
            disc(arr, float(px), float(py), 1.6, bot, 0.55, soft=1.2)
    elif kind == "confetti":
        glow(arr, 256, 180, 200, bot, 0.18 + 0.05 * math.sin(t))
        bits = (rgb("ff5a8a"), rgb("ffe040"), rgb("40e0ff"), rgb("c070ff"))
        for i in range(22):
            px = (41 * i + int(math.sin(t + i) * 18)) % W
            py = (19 * i + frame * 9 + i * 7) % H
            disc(arr, float(px), float(py), 3.5, bits[i % 4], 0.55, soft=2.2)
    else:
        glow(arr, 120 + math.sin(t) * 16, 160, 110, bot, 0.16)
        glow(arr, 390, 300, 130, rgb("80c878"), 0.12)
        disc(arr, 90, 360, 28, bot, 0.28, soft=12)
        disc(arr, 430, 390, 22, rgb("f0a0b0"), 0.24, soft=10)
    return arr


# --- glow -------------------------------------------------------------------

GLOWS = {
    "disco": "ff40c0",
    "laser": "40e0ff",
    "sparkle": "ffe060",
    "neon": "70ffb0",
    "champagne": "f0d090",
}


def paint_glow(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    t = phase(frame)
    color = rgb(GLOWS[kind])
    cx, cy = HEAD
    pulse = 0.26 + 0.08 * math.sin(t)
    glow(arr, cx, cy + 16, 190 + 14 * math.sin(t), color, pulse)
    glow(arr, cx, cy - 30, 100, color, pulse * 0.5)
    if kind == "laser":
        ellipse(arr, cx + math.cos(t) * 80, cy - 20, 160, 10, color, 0.18, soft=12)
        ellipse(arr, cx - math.sin(t) * 60, cy + 40, 10, 140, color, 0.14, soft=10)
    elif kind == "sparkle":
        for i in range(8):
            ang = t + i * 0.8
            disc(arr, cx + math.cos(ang) * 110, cy + math.sin(ang) * 80, 4, color, 0.45, soft=3)
    return arr


# --- panda ------------------------------------------------------------------

PANDAS = {
    "classic": {
        "fur": "f4efe6",
        "ink": "1a1a22",
        "belly": "fff8f0",
        "blush": "f0b0a4",
        "nose": "141418",
        "scale": 1.0,
    },
    "chubby": {
        "fur": "f6efe4",
        "ink": "242028",
        "belly": "ffe8d0",
        "blush": "f09888",
        "nose": "1c1818",
        "scale": 1.12,
    },
    "cub": {
        "fur": "f8f4ec",
        "ink": "2a2428",
        "belly": "fff8f0",
        "blush": "f0c0b0",
        "nose": "201818",
        "scale": 0.86,
    },
    "dancer": {
        "fur": "f0e8f4",
        "ink": "2a1838",
        "belly": "f8e0f0",
        "blush": "e878a8",
        "nose": "1a1020",
        "scale": 0.96,
    },
    "tuxedo": {
        "fur": "f8f6f0",
        "ink": "0c0c12",
        "belly": "ffffff",
        "blush": "e8a898",
        "nose": "08080c",
        "scale": 1.02,
    },
    "peach": {
        "fur": "f8e8d8",
        "ink": "4a2820",
        "belly": "ffd8c0",
        "blush": "f08070",
        "nose": "301818",
        "scale": 1.0,
    },
}


def paint_panda(kind: str, frame: int) -> np.ndarray:
    palette = PANDAS[kind]
    fur, ink, belly, blush, nose = (rgb(palette[k]) for k in ("fur", "ink", "belly", "blush", "nose"))
    scale = float(palette["scale"])
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    sway = math.sin(phase(frame)) * 4

    body_rx, body_ry = 118 * scale, 108 * scale
    ellipse(arr, cx, cy + 148 * scale, body_rx, body_ry, ink, 0.98, soft=14)
    ellipse(arr, cx, cy + 156 * scale, body_rx * 0.62, body_ry * 0.7, belly, 0.92, soft=14)
    if kind == "tuxedo":
        ellipse(arr, cx, cy + 150 * scale, 28, 70 * scale, fur, 0.9, soft=10)

    arm_y = cy + 128 * scale
    ellipse(arr, cx - 108 * scale + sway * 0.3, arm_y, 38 * scale, 70 * scale, ink, 0.96, soft=12)
    ellipse(arr, cx + 108 * scale + sway * 0.3, arm_y, 38 * scale, 70 * scale, ink, 0.96, soft=12)
    disc(arr, cx - 118 * scale + sway * 0.3, arm_y + 58 * scale, 22 * scale, ink, 0.95, soft=8)
    disc(arr, cx + 118 * scale + sway * 0.3, arm_y + 58 * scale, 22 * scale, ink, 0.95, soft=8)

    ear_r = 36 * (1.18 if kind == "cub" else 1.0) * scale
    disc(arr, cx - 86 * scale, cy - 96 * scale, ear_r, ink, 0.98, soft=9)
    disc(arr, cx + 86 * scale, cy - 96 * scale, ear_r, ink, 0.98, soft=9)
    disc(arr, cx - 86 * scale, cy - 94 * scale, ear_r * 0.42, blush, 0.28, soft=6)
    disc(arr, cx + 86 * scale, cy - 94 * scale, ear_r * 0.42, blush, 0.28, soft=6)

    head_r = 118 * scale
    disc(arr, cx, cy, head_r, fur, 0.99, soft=12)
    glow(arr, cx - 30, cy - 20, 50, rgb("ffffff"), 0.16)

    patch_rx, patch_ry = 34 * scale, 40 * scale
    ellipse(arr, cx - 42 * scale, cy - 6 * scale, patch_rx, patch_ry, ink, 0.98, soft=8)
    ellipse(arr, cx + 42 * scale, cy - 6 * scale, patch_rx, patch_ry, ink, 0.98, soft=8)

    ellipse(arr, cx, cy + 38 * scale, 48 * scale, 36 * scale, fur, 0.98, soft=10)
    ellipse(arr, cx, cy + 34 * scale, 40 * scale, 28 * scale, belly, 0.55, soft=10)
    disc(arr, cx - 52 * scale, cy + 28 * scale, 14 * scale, blush, 0.32, soft=8)
    disc(arr, cx + 52 * scale, cy + 28 * scale, 14 * scale, blush, 0.32, soft=8)
    ellipse(arr, cx, cy + 28 * scale, 14 * scale, 10 * scale, nose, 0.96, soft=4)
    disc(arr, cx - 3, cy + 24 * scale, 3.2, rgb("ffffff"), 0.45, soft=2)
    return arr


# --- mood -------------------------------------------------------------------

def paint_mood(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    t = phase(frame)
    closed = blink_amount(frame)
    white = rgb("ffffff")
    pupil = rgb("141418")
    shine = rgb("fff8e8")
    ink = rgb("1a1a22")
    pink = rgb("f07090")
    gold = rgb("ffe060")

    def eye(ex: float, ey: float, shut: float, heart: bool = False, spark: bool = False) -> None:
        if shut >= 0.9:
            ellipse(arr, ex, ey, 16, 3.5, ink, 0.9, soft=2.5)
            return
        ry = 16 * (1.0 - shut * 0.85)
        disc(arr, ex, ey, 15, white, 0.96, soft=4)
        if heart:
            disc(arr, ex, ey + 1, 9, pink, 0.95, soft=3)
            disc(arr, ex - 4, ey - 2, 5, pink, 0.9, soft=2)
            disc(arr, ex + 4, ey - 2, 5, pink, 0.9, soft=2)
            disc(arr, ex - 2, ey - 3, 2.2, shine, 0.7, soft=1.4)
        elif spark:
            disc(arr, ex, ey + 1, 8, gold, 0.95, soft=3)
            disc(arr, ex, ey + 1, 3.5, pupil, 0.9, soft=1.6)
            disc(arr, ex - 3, ey - 3, 2.4, shine, 0.8, soft=1.4)
        else:
            disc(arr, ex, ey + 1, 8.5, pupil, 0.96, soft=3)
            disc(arr, ex - 3, ey - 3, 3.2, shine, 0.85, soft=1.8)
        if shut > 0.4:
            ellipse(arr, ex, ey - 8, 16, 8 * shut, rgb("f4efe6"), 0.9, soft=4)

    if kind == "shades":
        glass = rgb("141820")
        rim = rgb("1a1a22")
        ellipse(arr, cx - 40, cy - 4, 28, 16, glass, 0.88, soft=5)
        ellipse(arr, cx + 40, cy - 4, 28, 16, glass, 0.88, soft=5)
        ellipse(arr, cx, cy - 6, 18, 4, rim, 0.9, soft=3)
        glow(arr, cx - 48, cy - 8, 10, rgb("40e0ff"), 0.28 + 0.08 * math.sin(t))
        glow(arr, cx + 32, cy - 8, 8, rgb("ff40c0"), 0.2)
    elif kind == "wink":
        eye(cx - 42, cy - 4, 0.0)
        eye(cx + 42, cy - 4, 1.0)
    elif kind == "heart":
        eye(cx - 42, cy - 4, closed, heart=True)
        eye(cx + 42, cy - 4, closed, heart=True)
    elif kind == "spark":
        eye(cx - 42, cy - 4, closed, spark=True)
        eye(cx + 42, cy - 4, closed, spark=True)
    elif kind == "sleepy":
        eye(cx - 42, cy - 2, 0.55)
        eye(cx + 42, cy - 2, 0.55)
    else:
        eye(cx - 42, cy - 4, closed)
        eye(cx + 42, cy - 4, closed)

    smile = 6 + 2 * math.sin(t)
    if kind == "sleepy":
        ellipse(arr, cx, cy + 52, 10, 3.5, ink, 0.55, soft=2.5)
    else:
        ellipse(arr, cx, cy + 54, 16, smile, ink, 0.0, soft=3)
        ellipse(arr, cx, cy + 50, 18, 5.5, ink, 0.55, soft=3)
        ellipse(arr, cx, cy + 48, 16, 3.2, rgb("f4efe6"), 0.7, soft=3)
    return arr


# --- fit --------------------------------------------------------------------

def paint_fit(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    t = phase(frame)
    sway = math.sin(t) * 4
    if kind == "cone":
        hat = rgb("ff4a7a")
        trim = rgb("ffe060")
        ellipse(arr, cx, cy - 118, 54, 14, hat, 0.92, soft=8)
        ellipse(arr, cx + sway * 0.3, cy - 168, 18, 56, hat, 0.9, soft=10)
        disc(arr, cx + sway * 0.3, cy - 214, 10, trim, 0.9, soft=4)
        disc(arr, cx - 20, cy - 118, 5, trim, 0.7, soft=3)
        disc(arr, cx + 18, cy - 116, 4, rgb("40e0ff"), 0.7, soft=3)
    elif kind == "bow":
        silk = rgb("c42848")
        ellipse(arr, cx - 28, cy + 92, 22, 14, silk, 0.9, soft=6)
        ellipse(arr, cx + 28, cy + 92, 22, 14, silk, 0.9, soft=6)
        disc(arr, cx, cy + 92, 9, silk, 0.95, soft=4)
        disc(arr, cx, cy + 90, 3.5, rgb("ffe060"), 0.65, soft=2)
    elif kind == "phones":
        band = rgb("2a2a32")
        cup = rgb("ff40c0")
        ellipse(arr, cx, cy - 70, 108, 70, band, 0.0, soft=8)
        ellipse(arr, cx, cy - 96, 92, 22, band, 0.85, soft=8)
        ellipse(arr, cx - 108, cy + 4, 22, 32, cup, 0.92, soft=8)
        ellipse(arr, cx + 108, cy + 4, 22, 32, cup, 0.92, soft=8)
        glow(arr, cx - 108, cy + 4, 16, rgb("40e0ff"), 0.22 + 0.08 * math.sin(t))
    elif kind == "lei":
        petals = (rgb("ff6a9a"), rgb("ffe060"), rgb("70e0c0"), rgb("ff9040"))
        for i, ang in enumerate(np.linspace(-2.4, 2.4, 11)):
            px = cx + math.sin(ang) * 92
            py = cy + 88 + math.cos(ang) * 18
            disc(arr, px, py, 12, petals[i % 4], 0.82, soft=6)
            disc(arr, px, py, 4, rgb("fff4d0"), 0.55, soft=3)
    elif kind == "crown":
        gold = rgb("ffe060")
        glow(arr, cx, cy - 128, 40, gold, 0.2 + 0.06 * math.sin(t))
        ellipse(arr, cx, cy - 118, 58, 14, gold, 0.88, soft=7)
        disc(arr, cx - 30, cy - 136, 8, gold, 0.9, soft=4)
        disc(arr, cx, cy - 148, 10, gold, 0.92, soft=4)
        disc(arr, cx + 30, cy - 136, 8, gold, 0.9, soft=4)
        disc(arr, cx, cy - 148, 4, rgb("fff8d0"), 0.75, soft=2)
    elif kind == "afro":
        hair = rgb("2a1830")
        for ox, oy, r in ((-70, -80, 48), (70, -80, 48), (0, -120, 56), (-40, -110, 42), (40, -110, 42), (-90, -40, 34), (90, -40, 34)):
            disc(arr, cx + ox, cy + oy, r, hair, 0.92, soft=14)
        glow(arr, cx, cy - 130, 40, rgb("ff40c0"), 0.12)
    return arr


# --- extra ------------------------------------------------------------------

def paint_extra(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame, amp=3.0)
    t = phase(frame)
    if kind == "confetti":
        bits = (rgb("ff5a8a"), rgb("ffe040"), rgb("40e0ff"), rgb("c070ff"), rgb("70ffb0"))
        for i in range(16):
            px = (cx - 160 + (i * 27 + math.sin(t + i) * 20)) % (W - 20) + 10
            py = (40 + i * 19 + frame * 11) % (H - 30)
            disc(arr, float(px), float(py), 3.8, bits[i % 5], 0.7, soft=2)
    elif kind == "balloon":
        color = rgb("ff4a7a")
        bx = cx + 150 + math.sin(t) * 8
        by = cy - 90 + math.cos(t) * 6
        ellipse(arr, bx, by, 28, 36, color, 0.92, soft=8)
        disc(arr, bx - 8, by - 10, 7, rgb("ffffff"), 0.35, soft=4)
        ellipse(arr, bx, by + 40, 4, 8, color, 0.7, soft=3)
        ellipse(arr, bx - 4, by + 70, 3, 28, rgb("f4efe6"), 0.45, soft=3)
    elif kind == "cocktail":
        glass = rgb("e8f4f8")
        drink = rgb("ff6a9a")
        gx, gy = cx + 138, cy + 70 + math.sin(t) * 3
        ellipse(arr, gx, gy, 22, 16, drink, 0.8, soft=6)
        ellipse(arr, gx, gy - 2, 22, 8, glass, 0.35, soft=5)
        ellipse(arr, gx, gy + 28, 3, 26, glass, 0.55, soft=3)
        ellipse(arr, gx, gy + 52, 14, 4, glass, 0.6, soft=3)
        disc(arr, gx + 10, gy - 18, 5, rgb("ffe060"), 0.7, soft=3)
    elif kind == "sparkler":
        gold = rgb("ffe060")
        sx, sy = cx - 146, cy + 40
        ellipse(arr, sx, sy + 30, 3, 36, rgb("c8a070"), 0.8, soft=3)
        glow(arr, sx, sy - 8, 28, gold, 0.35 + 0.1 * math.sin(t * 2))
        for i in range(10):
            ang = t * 2 + i * 0.7
            disc(arr, sx + math.cos(ang) * 18, sy - 8 + math.sin(ang) * 18, 2.4, gold, 0.7, soft=1.6)
    elif kind == "boombox":
        box = rgb("2a2430")
        accent = rgb("ff40c0")
        bx, by = cx + 150, cy + 86
        ellipse(arr, bx, by, 40, 22, box, 0.92, soft=7)
        disc(arr, bx - 16, by, 10, rgb("1a1a22"), 0.9, soft=4)
        disc(arr, bx + 16, by, 10, rgb("1a1a22"), 0.9, soft=4)
        glow(arr, bx - 16, by, 8, accent, 0.28 + 0.1 * math.sin(t * 2))
        glow(arr, bx + 16, by, 8, rgb("40e0ff"), 0.24 + 0.1 * math.cos(t * 2))
    return arr


# --- catalog ----------------------------------------------------------------

TRAIT_SPEC = {
    "venue": [
        ("disco", "Disco Night", 16),
        ("neon", "Neon Club", 14),
        ("bamboo", "Bamboo Lounge", 14),
        ("rooftop", "Rooftop Glow", 12),
        ("candy", "Candy Rave", 12),
        ("moonlight", "Moonlight", 12),
        ("confetti", "Confetti Hall", 10),
        ("garden", "Garden Party", 10),
    ],
    "glow": [
        ("none", "No glow", 22),
        ("disco", "Disco Pulse", 16),
        ("laser", "Laser Sweep", 14),
        ("sparkle", "Sparkle Burst", 14),
        ("neon", "Neon Ring", 12),
        ("champagne", "Champagne Haze", 12),
    ],
    "panda": [
        ("classic", "Classic", 20),
        ("chubby", "Chubby", 18),
        ("cub", "Cub", 16),
        ("dancer", "Dancer", 16),
        ("tuxedo", "Tuxedo", 16),
        ("peach", "Peach", 14),
    ],
    "mood": [
        ("blink", "Blink", 22),
        ("wink", "Wink", 18),
        ("shades", "Shades", 16),
        ("heart", "Heart", 16),
        ("sleepy", "Sleepy", 14),
        ("spark", "Spark", 14),
    ],
    "fit": [
        ("none", "Bare head", 22),
        ("cone", "Party Hat", 16),
        ("bow", "Bowtie", 14),
        ("phones", "Headphones", 14),
        ("lei", "Lei", 12),
        ("crown", "Tiny Crown", 12),
        ("afro", "Disco Afro", 10),
    ],
    "extra": [
        ("none", "None", 22),
        ("confetti", "Confetti", 16),
        ("balloon", "Balloon", 14),
        ("cocktail", "Cocktail", 14),
        ("sparkler", "Sparkler", 12),
        ("boombox", "Boombox", 10),
    ],
}

PAINTERS = {
    "venue": {k: (lambda kind: (lambda frame, k=kind: paint_venue(k, frame)))(k) for k in VENUES},
    "glow": {k: (lambda kind: (lambda frame, k=kind: paint_glow(k, frame)))(k) for k in GLOWS},
    "panda": {k: (lambda kind: (lambda frame, k=kind: paint_panda(k, frame)))(k) for k in PANDAS},
    "mood": {k: (lambda kind: (lambda frame, k=kind: paint_mood(k, frame)))(k) for k in ("blink", "wink", "shades", "heart", "sleepy", "spark")},
    "fit": {k: (lambda kind: (lambda frame, k=kind: paint_fit(k, frame)))(k) for k in ("cone", "bow", "phones", "lei", "crown", "afro")},
    "extra": {k: (lambda kind: (lambda frame, k=kind: paint_extra(k, frame)))(k) for k in ("confetti", "balloon", "cocktail", "sparkler", "boombox")},
}

STACK = ("venue", "glow", "panda", "mood", "fit", "extra")

SIGNATURES = [
    {"venue": "disco", "glow": "disco", "panda": "classic", "mood": "blink", "fit": "cone", "extra": "confetti"},
    {"venue": "neon", "glow": "laser", "panda": "dancer", "mood": "shades", "fit": "phones", "extra": "boombox"},
    {"venue": "bamboo", "glow": "neon", "panda": "chubby", "mood": "heart", "fit": "lei", "extra": "balloon"},
    {"venue": "rooftop", "glow": "none", "panda": "tuxedo", "mood": "wink", "fit": "bow", "extra": "cocktail"},
    {"venue": "candy", "glow": "sparkle", "panda": "cub", "mood": "spark", "fit": "crown", "extra": "none"},
    {"venue": "moonlight", "glow": "champagne", "panda": "peach", "mood": "sleepy", "fit": "none", "extra": "sparkler"},
    {"venue": "confetti", "glow": "disco", "panda": "classic", "mood": "shades", "fit": "afro", "extra": "confetti"},
    {"venue": "garden", "glow": "sparkle", "panda": "chubby", "mood": "blink", "fit": "cone", "extra": "balloon"},
    {"venue": "disco", "glow": "laser", "panda": "dancer", "mood": "heart", "fit": "crown", "extra": "sparkler"},
    {"venue": "neon", "glow": "neon", "panda": "cub", "mood": "wink", "fit": "phones", "extra": "none"},
    {"venue": "bamboo", "glow": "none", "panda": "peach", "mood": "sleepy", "fit": "lei", "extra": "cocktail"},
    {"venue": "rooftop", "glow": "champagne", "panda": "tuxedo", "mood": "blink", "fit": "bow", "extra": "boombox"},
    {"venue": "candy", "glow": "disco", "panda": "classic", "mood": "spark", "fit": "afro", "extra": "confetti"},
    {"venue": "moonlight", "glow": "laser", "panda": "dancer", "mood": "shades", "fit": "none", "extra": "balloon"},
    {"venue": "confetti", "glow": "sparkle", "panda": "chubby", "mood": "heart", "fit": "cone", "extra": "none"},
    {"venue": "garden", "glow": "champagne", "panda": "cub", "mood": "blink", "fit": "crown", "extra": "sparkler"},
]

TRAIT_LABELS = (
    ("venue", "Venue"),
    ("glow", "Glow"),
    ("panda", "Panda"),
    ("mood", "Mood"),
    ("fit", "Fit"),
    ("extra", "Extra"),
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
        "name": "Party Pandas",
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
                "name": f"Party Panda #{index}",
                "image": f"/party-pandas-preview/{index}.gif",
                "attributes": [
                    {"trait_type": label, "value": name_of(key, selection[key])}
                    for key, label in TRAIT_LABELS
                ],
            }
        )
    (META_DIR / "party-pandas-samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")


COLLECTION_DESCRIPTION = (
    "Party Pandas is a 4,444-piece collection of looping party-panda PFP GIFs on Base. "
    "Each panda is stacked from six layers — venue, glow, panda, mood, fit, and extra — "
    "then flattened onto one 12-frame GIF. Disco lights sweep. Hats bounce. Confetti never lands."
)

COLLECTION_STORY = (
    "Party Pandas never sit still.\n\n"
    "A 4,444-piece collection of looping party-panda PFP GIFs on Base. "
    "Each panda is stacked from six layers — venue, glow, panda, mood, fit, and extra — "
    "then flattened onto one 12-frame GIF, the same clock Loopkins uses. "
    "Clubs pulse. Eyes blink. Balloons drift. Soft edges only.\n\n"
    "Minting on Base (chain ID 8453). Gas is ETH. 0.004 ETH to mint."
)


def panoramic_wash(width: int, height: int, frame: int = 0) -> Image.Image:
    left = np.asarray(to_image(paint_venue("disco", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    mid = np.asarray(to_image(paint_venue("candy", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    right = np.asarray(to_image(paint_venue("neon", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
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
    ImageDraw.Draw(shadow).rounded_rectangle((8, 14, size + 8, size + 18), radius=radius, fill=(16, 6, 18, 90))
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
    (META_DIR / "party-pandas-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "party-pandas.json").write_text(
        json.dumps(
            {
                "name": "Party Pandas",
                "symbol": "PAND",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-party-pandas.gif",
                "featured_image": "/brand/featured-party-pandas.jpg",
                "banner_image": "/brand/banner-party-pandas.png",
                "opensea_banner_image": "/brand/banner-party-pandas-opensea.jpg",
                "external_link": "/party-pandas",
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
    ImageDraw.Draw(ring).ellipse((10, 10, SIZE - 10, SIZE - 10), outline=(255, 64, 192, 220), width=10)
    logo = Image.alpha_composite(logo, ring)
    logo.resize((512, 512), Image.Resampling.LANCZOS).save(BRAND_DIR / "logo-party-pandas.png")
    save_apng([frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames], BRAND_DIR / "logo-party-pandas-loop.png")

    site_banner = lineup_banner(1500, 560, portraits[:5])
    site_banner.convert("RGB").save(BRAND_DIR / "banner-party-pandas.png", quality=94)

    opensea_banner = lineup_banner(2800, 700, portraits)
    opensea_banner.convert("RGB").save(BRAND_DIR / "banner-party-pandas-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800, frame=8)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=64)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=64)
    featured.convert("RGB").save(BRAND_DIR / "featured-party-pandas.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(gif_frames, BRAND_DIR / "collection-party-pandas.gif", DURATION_MS)
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true", help="Rebuild logo, banners, and listing copy")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Party Pandas brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Party Pandas trait loops…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
