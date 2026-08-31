#!/usr/bin/env python3
"""Paint Inklings — smooth ink-wash PFP layers for an OpenSea Drop on Ink.

Every trait is a 16-frame APNG on a shared 640 canvas and 90ms clock.
Character layers share one breathe so a stacked preview stays locked together.
Paper and bloom move on their own washes. Soft edges only — no pixel art.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gif_bake import save_loop_gif  # noqa: E402

TRAIT_DIR = ROOT / "public" / "inklings-traits"
PREVIEW_DIR = ROOT / "public" / "inklings-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"

SIZE = 640
FRAMES = 16
DURATION_MS = 90
H, W = SIZE, SIZE

HEAD = (320.0, 292.0)


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
    soft: float = 14.0,
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
    soft: float = 12.0,
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


def grain(seed: int, amp: float = 0.045) -> np.ndarray:
    rng = np.random.default_rng(seed)
    small = (rng.random((SIZE // 18, SIZE // 18)) * 2 - 1).astype(np.float32)
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


def bob(frame: int, amp: float = 6.0) -> float:
    return math.sin(2 * math.pi * frame / FRAMES) * amp


def phase(frame: int) -> float:
    return 2.0 * math.pi * frame / FRAMES


def blink_amount(frame: int, closed_at: int = 11) -> float:
    dist = min(abs(frame - closed_at), abs(frame - closed_at + FRAMES), abs(frame - closed_at - FRAMES))
    if dist == 0:
        return 1.0
    if dist == 1:
        return 0.55
    return 0.0


# --- paper ------------------------------------------------------------------

PAPERS = {
    "indigo": ("1a1028", "3a2a68", "6a4a9a", 7),
    "peach": ("3a2418", "c47858", "f0c8a0", 11),
    "celadon": ("1a2a24", "4a7868", "c8e0c8", 13),
    "charcoal": ("141218", "2a2830", "6a6670", 17),
    "rose": ("2a1820", "8a4a58", "e8b8b0", 19),
    "storm": ("1c2430", "3a4a58", "90a0b0", 23),
    "wine": ("241018", "6a2038", "c07080", 29),
    "cream": ("d8c8a8", "f0e6d0", "fff8ec", 31),
}


def paint_paper(kind: str, frame: int) -> np.ndarray:
    top_h, mid_h, bot_h, seed = PAPERS[kind]
    xx, yy = grid()
    t = phase(frame)
    top, mid, bot = rgb(top_h), rgb(mid_h), rgb(bot_h)
    v = yy / (H - 1)
    low = mix(top, mid, v / 0.55)
    high = mix(mid, bot, (v - 0.55) / 0.45)
    wash = np.where((v < 0.55)[..., None], low, high)
    arr = blank()
    arr[..., :3] = wash
    arr[..., 3] = 1.0
    texture = grain(seed, 0.05)
    arr[..., :3] = np.clip(arr[..., :3] + texture[..., None], 0.0, 1.0)
    drift_x = 320 + math.sin(t * 0.7) * 36
    drift_y = 180 + math.cos(t * 0.5) * 22
    glow(arr, drift_x, drift_y, 220, bot, 0.16 + 0.05 * math.sin(t))
    glow(arr, 480 - math.cos(t) * 20, 480, 180, mid, 0.10)
    return arr


# --- bloom ------------------------------------------------------------------

BLOOMS = {
    "violet": "b08cff",
    "gold": "e8c87a",
    "teal": "6ad4c0",
    "coral": "f09078",
    "silver": "d8d4e8",
}


def paint_bloom(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    t = phase(frame)
    color = rgb(BLOOMS[kind])
    cx, cy = HEAD
    pulse = 0.28 + 0.08 * math.sin(t)
    glow(arr, cx, cy + 10, 210 + 12 * math.sin(t), color, pulse)
    glow(arr, cx, cy - 40, 120, color, pulse * 0.55)
    return arr


# --- visages ----------------------------------------------------------------

VISAGES = {
    "fox": {
        "fur": "c46a32",
        "shade": "8a3e18",
        "cream": "f3d7b0",
        "blush": "e89a8a",
        "dark": "5a2e16",
        "accent": "e8a090",
    },
    "crane": {
        "fur": "f4efe6",
        "shade": "c8b8a0",
        "cream": "eadcc4",
        "blush": "e8b4b0",
        "dark": "4a5568",
        "accent": "c43c3c",
    },
    "koi": {
        "fur": "e07a3a",
        "shade": "b04a20",
        "cream": "f6e8c8",
        "blush": "f0a090",
        "dark": "2a2420",
        "accent": "f8f4ea",
    },
    "cat": {
        "fur": "c8b8a8",
        "shade": "8a7a6c",
        "cream": "efe4d4",
        "blush": "e8a8a0",
        "dark": "4a3a32",
        "accent": "e8b0a4",
    },
    "moth": {
        "fur": "c4b0d4",
        "shade": "8a7a9a",
        "cream": "efe8f0",
        "blush": "d4a0c0",
        "dark": "3a2a48",
        "accent": "b090c8",
    },
    "moon": {
        "fur": "e8e4dc",
        "shade": "b8b0a4",
        "cream": "f4f0e8",
        "blush": "e0c8b0",
        "dark": "9a9488",
        "accent": "d4b86a",
    },
    "otter": {
        "fur": "8a5a3a",
        "shade": "5a3820",
        "cream": "f0e0c8",
        "blush": "d49078",
        "dark": "4a2e1e",
        "accent": "c89068",
    },
    "hare": {
        "fur": "c4a888",
        "shade": "8a6e52",
        "cream": "f2e6d4",
        "blush": "e8b0a4",
        "dark": "5a4030",
        "accent": "d4b898",
    },
}


def paint_visage(kind: str, frame: int) -> np.ndarray:
    palette = VISAGES[kind]
    fur, shade, cream, blush, dark, accent = (rgb(palette[k]) for k in ("fur", "shade", "cream", "blush", "dark", "accent"))
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    ellipse(arr, cx, cy + 168, 168, 92, shade, 0.95, soft=22)
    ellipse(arr, cx, cy + 160, 150, 82, fur, 0.98, soft=18)
    ellipse(arr, cx, cy + 172, 70, 48, cream, 0.88, soft=16)
    ellipse(arr, cx, cy + 86, 52, 46, fur, 0.96, soft=14)

    if kind == "fox":
        ellipse(arr, cx - 78, cy - 118, 34, 72, fur, 0.98, soft=12)
        ellipse(arr, cx + 78, cy - 118, 34, 72, fur, 0.98, soft=12)
        ellipse(arr, cx - 78, cy - 112, 16, 40, accent, 0.9, soft=10)
        ellipse(arr, cx + 78, cy - 112, 16, 40, accent, 0.9, soft=10)
        ellipse(arr, cx, cy - 8, 118, 128, fur, 0.99, soft=18)
        glow(arr, cx - 40, cy + 10, 50, shade, 0.18)
        glow(arr, cx + 40, cy + 10, 50, shade, 0.18)
        ellipse(arr, cx, cy + 38, 62, 48, cream, 0.96, soft=14)
        disc(arr, cx - 48, cy + 18, 26, blush, 0.28, soft=16)
        disc(arr, cx + 48, cy + 18, 26, blush, 0.28, soft=16)
        ellipse(arr, cx, cy + 28, 14, 10, dark, 0.88, soft=6)
        ellipse(arr, cx, cy + 58, 22, 8, dark, 0.35, soft=6)
    elif kind == "crane":
        ellipse(arr, cx, cy - 8, 104, 122, fur, 0.99, soft=18)
        glow(arr, cx, cy + 16, 70, shade, 0.16)
        disc(arr, cx, cy - 108, 28, accent, 0.92, soft=12)
        disc(arr, cx, cy - 108, 14, rgb("f4efe6"), 0.55, soft=8)
        ellipse(arr, cx, cy + 42, 18, 28, dark, 0.88, soft=8)
        disc(arr, cx - 40, cy + 16, 22, blush, 0.22, soft=14)
        disc(arr, cx + 40, cy + 16, 22, blush, 0.22, soft=14)
        ellipse(arr, cx, cy + 62, 16, 5, dark, 0.28, soft=5)
    elif kind == "koi":
        ellipse(arr, cx, cy - 4, 124, 126, cream, 0.99, soft=18)
        disc(arr, cx - 46, cy - 36, 48, fur, 0.92, soft=16)
        disc(arr, cx + 52, cy + 18, 40, fur, 0.88, soft=16)
        disc(arr, cx + 20, cy - 70, 22, dark, 0.55, soft=12)
        glow(arr, cx, cy + 20, 60, blush, 0.16)
        disc(arr, cx - 50, cy + 16, 24, blush, 0.24, soft=14)
        disc(arr, cx + 50, cy + 16, 24, blush, 0.24, soft=14)
        ellipse(arr, cx, cy + 32, 12, 8, dark, 0.8, soft=6)
        ellipse(arr, cx - 70, cy + 28, 28, 5, dark, 0.28, soft=6)
        ellipse(arr, cx + 70, cy + 28, 28, 5, dark, 0.28, soft=6)
        ellipse(arr, cx, cy + 58, 24, 8, dark, 0.28, soft=6)
    elif kind == "cat":
        ellipse(arr, cx - 72, cy - 108, 32, 48, fur, 0.98, soft=12)
        ellipse(arr, cx + 72, cy - 108, 32, 48, fur, 0.98, soft=12)
        ellipse(arr, cx - 72, cy - 104, 14, 24, accent, 0.88, soft=9)
        ellipse(arr, cx + 72, cy - 104, 14, 24, accent, 0.88, soft=9)
        ellipse(arr, cx, cy - 6, 120, 124, fur, 0.99, soft=18)
        glow(arr, cx, cy + 18, 64, shade, 0.14)
        ellipse(arr, cx, cy + 36, 52, 40, cream, 0.9, soft=14)
        disc(arr, cx - 46, cy + 16, 24, blush, 0.26, soft=14)
        disc(arr, cx + 46, cy + 16, 24, blush, 0.26, soft=14)
        ellipse(arr, cx, cy + 26, 11, 8, accent, 0.92, soft=5)
        ellipse(arr, cx, cy + 56, 18, 6, dark, 0.3, soft=5)
    elif kind == "moth":
        ellipse(arr, cx - 110, cy - 20, 70, 110, accent, 0.55, soft=22)
        ellipse(arr, cx + 110, cy - 20, 70, 110, accent, 0.55, soft=22)
        ellipse(arr, cx - 96, cy - 140, 10, 56, shade, 0.7, soft=10)
        ellipse(arr, cx + 96, cy - 140, 10, 56, shade, 0.7, soft=10)
        disc(arr, cx - 96, cy - 188, 10, cream, 0.7, soft=8)
        disc(arr, cx + 96, cy - 188, 10, cream, 0.7, soft=8)
        ellipse(arr, cx, cy - 4, 116, 122, fur, 0.99, soft=18)
        glow(arr, cx, cy + 16, 60, shade, 0.18)
        disc(arr, cx - 44, cy + 18, 24, blush, 0.22, soft=14)
        disc(arr, cx + 44, cy + 18, 24, blush, 0.22, soft=14)
        ellipse(arr, cx, cy + 30, 10, 7, dark, 0.7, soft=5)
        ellipse(arr, cx, cy + 56, 16, 5, dark, 0.24, soft=5)
    elif kind == "moon":
        ellipse(arr, cx, cy - 6, 122, 126, fur, 0.99, soft=20)
        glow(arr, cx - 30, cy - 20, 80, cream, 0.22)
        glow(arr, cx + 40, cy + 24, 70, shade, 0.14)
        ellipse(arr, cx + 36, cy + 8, 34, 52, accent, 0.28, soft=16)
        disc(arr, cx - 46, cy + 18, 24, blush, 0.2, soft=16)
        disc(arr, cx + 46, cy + 18, 24, blush, 0.2, soft=16)
        ellipse(arr, cx, cy + 30, 10, 7, dark, 0.45, soft=6)
        ellipse(arr, cx, cy + 56, 16, 5, dark, 0.22, soft=5)
    elif kind == "otter":
        ellipse(arr, cx - 62, cy - 96, 28, 28, fur, 0.96, soft=12)
        ellipse(arr, cx + 62, cy - 96, 28, 28, fur, 0.96, soft=12)
        ellipse(arr, cx, cy - 4, 122, 124, fur, 0.99, soft=18)
        ellipse(arr, cx, cy + 28, 70, 58, cream, 0.94, soft=16)
        glow(arr, cx, cy + 10, 56, shade, 0.16)
        disc(arr, cx - 48, cy + 14, 24, blush, 0.24, soft=14)
        disc(arr, cx + 48, cy + 14, 24, blush, 0.24, soft=14)
        ellipse(arr, cx, cy + 26, 13, 9, dark, 0.86, soft=6)
        ellipse(arr, cx - 74, cy + 24, 30, 4, dark, 0.26, soft=5)
        ellipse(arr, cx + 74, cy + 24, 30, 4, dark, 0.26, soft=5)
        ellipse(arr, cx, cy + 58, 20, 7, dark, 0.3, soft=5)
    else:  # hare
        ellipse(arr, cx - 58, cy - 150, 26, 88, fur, 0.98, soft=14)
        ellipse(arr, cx + 58, cy - 150, 26, 88, fur, 0.98, soft=14)
        ellipse(arr, cx - 58, cy - 146, 12, 58, accent, 0.82, soft=10)
        ellipse(arr, cx + 58, cy - 146, 12, 58, accent, 0.82, soft=10)
        ellipse(arr, cx, cy - 6, 118, 124, fur, 0.99, soft=18)
        glow(arr, cx, cy + 16, 60, shade, 0.14)
        ellipse(arr, cx, cy + 36, 54, 42, cream, 0.9, soft=14)
        disc(arr, cx - 46, cy + 16, 24, blush, 0.26, soft=14)
        disc(arr, cx + 46, cy + 16, 24, blush, 0.26, soft=14)
        ellipse(arr, cx, cy + 28, 11, 8, accent, 0.9, soft=5)
        ellipse(arr, cx, cy + 56, 18, 6, dark, 0.28, soft=5)
    return arr


# --- gaze -------------------------------------------------------------------

def paint_gaze(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    ly, ry = cx - 38, cx + 38
    ey = cy - 8
    closed = blink_amount(frame)
    left_closed = 1.0 if kind == "wink" else closed
    right_closed = closed
    if kind == "sleepy":
        left_closed = max(left_closed, 0.42)
        right_closed = max(right_closed, 0.42)
    if kind == "lidded":
        left_closed = max(left_closed, 0.28)
        right_closed = max(right_closed, 0.28)

    iris = rgb("3a2a68") if kind != "ember" else rgb("e07040")
    if kind == "dew":
        iris = rgb("3a5a78")
    sclera = rgb("f8f4ea")
    pupil = rgb("1a1020")
    shine = rgb("ffffff")
    lid = rgb("4a3028")

    def one_eye(ex: float, shut: float) -> None:
        open_amt = 1.0 - shut
        ry_eye = 18.0 * max(open_amt, 0.08)
        if shut >= 0.92:
            ellipse(arr, ex, ey, 20, 4, lid, 0.75, soft=5)
            return
        ellipse(arr, ex, ey, 22, ry_eye, sclera, 0.96, soft=6)
        iris_y = ey + (2 if kind == "lidded" else 0)
        ellipse(arr, ex, iris_y, 12, 12 * open_amt, iris, 0.96, soft=5)
        ellipse(arr, ex, iris_y, 6, 6 * open_amt, pupil, 0.94, soft=3)
        if kind == "ember":
            glow(arr, ex, iris_y, 16, rgb("ff8a50"), 0.35 * open_amt)
        disc(arr, ex - 4, ey - 5 * open_amt, 3.4, shine, 0.85 * open_amt, soft=3)
        if kind == "dew":
            disc(arr, ex + 5, ey + 4 * open_amt, 2.2, shine, 0.7 * open_amt, soft=2)
            disc(arr, ex, ey + 16, 3.0, rgb("c8d8e8"), 0.35 * open_amt, soft=4)
        if kind in ("lidded", "sleepy"):
            ellipse(arr, ex, ey - ry_eye * 0.7, 22, 7, lid, 0.28, soft=6)

    one_eye(ly, left_closed)
    one_eye(ry, right_closed)
    return arr


# --- marks ------------------------------------------------------------------

def paint_mark(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    t = phase(frame)
    ink = rgb("1a1028")
    red = rgb("c43c3c")
    if kind == "splash":
        disc(arr, cx + 86, cy + 48, 28, ink, 0.42, soft=16)
        disc(arr, cx + 108, cy + 62, 12, ink, 0.32, soft=10)
        disc(arr, cx + 70, cy + 70, 9, ink, 0.28, soft=8)
        disc(arr, cx - 96, cy - 20, 16, ink, 0.22, soft=12)
    elif kind == "drip":
        drip = 18 + 6 * math.sin(t)
        ellipse(arr, cx + 72, cy + 20, 10, 16, ink, 0.4, soft=10)
        ellipse(arr, cx + 72, cy + 48 + drip * 0.4, 7, 22 + drip, ink, 0.34, soft=10)
        disc(arr, cx + 72, cy + 78 + drip, 8, ink, 0.3, soft=8)
    elif kind == "seal":
        ellipse(arr, cx + 92, cy + 70, 26, 26, red, 0.55, soft=10)
        ellipse(arr, cx + 92, cy + 70, 16, 16, red, 0.0, soft=6)
        glow(arr, cx + 92, cy + 70, 18, red, 0.2)
        ellipse(arr, cx + 92, cy + 70, 8, 14, rgb("f6efe4"), 0.35, soft=5)
    elif kind == "streak":
        ellipse(arr, cx - 20, cy - 70, 90, 16, ink, 0.18, soft=18)
        ellipse(arr, cx + 10, cy - 58, 70, 10, ink, 0.14, soft=14)
    return arr


# --- adorn ------------------------------------------------------------------

def paint_adorn(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    t = phase(frame)
    sway = math.sin(t) * 6
    if kind == "flow":
        hair = rgb("2a1840")
        shine = rgb("6a4a8a")
        ellipse(arr, cx - 110 + sway * 0.3, cy + 20, 56, 130, hair, 0.88, soft=20)
        ellipse(arr, cx + 110 + sway * 0.3, cy + 20, 56, 130, hair, 0.88, soft=20)
        ellipse(arr, cx, cy - 118, 100, 46, hair, 0.86, soft=18)
        glow(arr, cx - 90, cy + 10, 40, shine, 0.18)
        glow(arr, cx + 90, cy + 10, 40, shine, 0.18)
    elif kind == "bun":
        silk = rgb("2a1840")
        pin = rgb("e8c87a")
        ellipse(arr, cx, cy - 128, 48, 42, silk, 0.94, soft=14)
        disc(arr, cx, cy - 136, 28, rgb("3a2460"), 0.8, soft=12)
        disc(arr, cx + 2, cy - 140, 8, pin, 0.8, soft=6)
        ellipse(arr, cx - 92, cy - 20, 36, 80, silk, 0.55, soft=16)
        ellipse(arr, cx + 92, cy - 20, 36, 80, silk, 0.55, soft=16)
    elif kind == "ribbon":
        ribbon = rgb("c43c3c")
        ellipse(arr, cx - 8, cy - 108, 70, 14, ribbon, 0.82, soft=10)
        ellipse(arr, cx - 70 + sway, cy - 40, 18, 70, ribbon, 0.7, soft=12)
        ellipse(arr, cx + 64 + sway, cy - 36, 16, 64, ribbon, 0.7, soft=12)
        disc(arr, cx, cy - 110, 12, rgb("e8c87a"), 0.7, soft=6)
    elif kind == "crown":
        gold = rgb("e8c87a")
        glow(arr, cx, cy - 124, 50, gold, 0.22 + 0.06 * math.sin(t))
        ellipse(arr, cx, cy - 118, 70, 18, gold, 0.72, soft=10)
        disc(arr, cx - 36, cy - 138, 10, gold, 0.8, soft=6)
        disc(arr, cx, cy - 148, 12, gold, 0.85, soft=6)
        disc(arr, cx + 36, cy - 138, 10, gold, 0.8, soft=6)
        disc(arr, cx, cy - 148, 5, rgb("fff4d0"), 0.7, soft=4)
    elif kind == "hood":
        cloth = rgb("2a1848")
        lining = rgb("4a3068")
        ellipse(arr, cx, cy - 20, 150, 160, cloth, 0.92, soft=20)
        xx, yy = grid()
        opening = np.sqrt(((xx - cx) / 104) ** 2 + ((yy - (cy + 8)) / 112) ** 2)
        cut = smoothstep(0.92, 1.08, opening)
        arr[..., 3] *= cut
        ellipse(arr, cx, cy - 118, 120, 40, lining, 0.55, soft=16)
        arr[..., 3][yy > cy + 70] *= 0.15
    return arr


# --- catalog ----------------------------------------------------------------

TRAIT_SPEC = {
    "paper": [
        ("indigo", "Indigo Night", 16),
        ("peach", "Peach Dusk", 14),
        ("celadon", "Celadon Garden", 14),
        ("charcoal", "Charcoal Wash", 12),
        ("rose", "Rose Gold", 12),
        ("storm", "Storm Grey", 12),
        ("wine", "Wine Paper", 10),
        ("cream", "Cream Rice", 10),
    ],
    "bloom": [
        ("none", "No bloom", 22),
        ("violet", "Violet Haze", 16),
        ("gold", "Gold Wash", 14),
        ("teal", "Teal Mist", 14),
        ("coral", "Coral Glow", 12),
        ("silver", "Silver Veil", 12),
    ],
    "visage": [
        ("fox", "Fox", 16),
        ("crane", "Crane", 14),
        ("koi", "Koi", 14),
        ("cat", "Cat", 14),
        ("moth", "Moth", 12),
        ("moon", "Moon", 12),
        ("otter", "Otter", 10),
        ("hare", "Hare", 8),
    ],
    "gaze": [
        ("bright", "Bright", 22),
        ("lidded", "Lidded", 18),
        ("sleepy", "Sleepy", 16),
        ("wink", "Wink", 16),
        ("ember", "Ember", 14),
        ("dew", "Dew", 14),
    ],
    "mark": [
        ("none", "Clean face", 34),
        ("splash", "Ink Splash", 16),
        ("drip", "Slow Drip", 14),
        ("seal", "Red Seal", 12),
        ("streak", "Brush Streak", 12),
    ],
    "adorn": [
        ("none", "Bare head", 22),
        ("flow", "Flow Hair", 16),
        ("bun", "Silk Bun", 14),
        ("ribbon", "Ink Ribbon", 14),
        ("crown", "Soft Crown", 12),
        ("hood", "Wash Hood", 10),
    ],
}

PAINTERS = {
    "paper": {k: (lambda kind: (lambda frame, k=kind: paint_paper(k, frame)))(k) for k in PAPERS},
    "bloom": {k: (lambda kind: (lambda frame, k=kind: paint_bloom(k, frame)))(k) for k in BLOOMS},
    "visage": {k: (lambda kind: (lambda frame, k=kind: paint_visage(k, frame)))(k) for k in VISAGES},
    "gaze": {k: (lambda kind: (lambda frame, k=kind: paint_gaze(k, frame)))(k) for k in ("bright", "lidded", "sleepy", "wink", "ember", "dew")},
    "mark": {k: (lambda kind: (lambda frame, k=kind: paint_mark(k, frame)))(k) for k in ("splash", "drip", "seal", "streak")},
    "adorn": {k: (lambda kind: (lambda frame, k=kind: paint_adorn(k, frame)))(k) for k in ("flow", "bun", "ribbon", "crown", "hood")},
}

STACK = ("paper", "bloom", "visage", "gaze", "mark", "adorn")

SIGNATURES = [
    {"paper": "indigo", "bloom": "violet", "visage": "fox", "gaze": "bright", "mark": "none", "adorn": "flow"},
    {"paper": "peach", "bloom": "gold", "visage": "crane", "gaze": "lidded", "mark": "seal", "adorn": "bun"},
    {"paper": "celadon", "bloom": "teal", "visage": "koi", "gaze": "dew", "mark": "splash", "adorn": "none"},
    {"paper": "charcoal", "bloom": "none", "visage": "cat", "gaze": "wink", "mark": "drip", "adorn": "ribbon"},
    {"paper": "rose", "bloom": "coral", "visage": "moth", "gaze": "ember", "mark": "none", "adorn": "hood"},
    {"paper": "storm", "bloom": "silver", "visage": "moon", "gaze": "sleepy", "mark": "streak", "adorn": "crown"},
    {"paper": "wine", "bloom": "gold", "visage": "otter", "gaze": "bright", "mark": "seal", "adorn": "flow"},
    {"paper": "cream", "bloom": "violet", "visage": "hare", "gaze": "dew", "mark": "none", "adorn": "bun"},
    {"paper": "indigo", "bloom": "silver", "visage": "crane", "gaze": "ember", "mark": "streak", "adorn": "hood"},
    {"paper": "peach", "bloom": "coral", "visage": "fox", "gaze": "wink", "mark": "splash", "adorn": "crown"},
    {"paper": "celadon", "bloom": "none", "visage": "otter", "gaze": "lidded", "mark": "none", "adorn": "ribbon"},
    {"paper": "charcoal", "bloom": "violet", "visage": "moth", "gaze": "bright", "mark": "drip", "adorn": "flow"},
    {"paper": "rose", "bloom": "gold", "visage": "moon", "gaze": "dew", "mark": "seal", "adorn": "none"},
    {"paper": "storm", "bloom": "teal", "visage": "cat", "gaze": "sleepy", "mark": "none", "adorn": "bun"},
    {"paper": "wine", "bloom": "coral", "visage": "hare", "gaze": "ember", "mark": "splash", "adorn": "hood"},
    {"paper": "cream", "bloom": "gold", "visage": "koi", "gaze": "bright", "mark": "streak", "adorn": "crown"},
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
        "name": "Inklings",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a soft ink-wash APNG. Studio stacks them live. Minted tokens flatten to GIF.",
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
                "name": f"Inkling #{index}",
                "image": f"/inklings-preview/{index}.gif",
                "attributes": [
                    {"trait_type": label, "value": name_of(key, selection[key])}
                    for key, label in (
                        ("paper", "Paper"),
                        ("bloom", "Bloom"),
                        ("visage", "Visage"),
                        ("gaze", "Gaze"),
                        ("mark", "Mark"),
                        ("adorn", "Adorn"),
                    )
                ],
            }
        )
    (META_DIR / "inklings-samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")


def build_brand() -> None:
    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    logo_frames = compose_selection(SIGNATURES[0])
    logo = logo_frames[0].copy()
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse((28, 28, SIZE - 28, SIZE - 28), fill=255)
    logo.putalpha(Image.composite(logo.split()[-1], Image.new("L", (SIZE, SIZE), 0), mask))
    logo.save(BRAND_DIR / "logo-inklings.png")
    save_apng(logo_frames, BRAND_DIR / "logo-inklings-loop.png")

    banner = Image.new("RGBA", (1500, 560), (26, 16, 40, 255))
    for i, paper_id in enumerate(("indigo", "peach", "celadon")):
        paper = to_image(paint_paper(paper_id, 0)).resize((520, 520), Image.Resampling.LANCZOS)
        banner.alpha_composite(paper, (i * 490 - 20, 20))
    for i, sel in enumerate((SIGNATURES[0], SIGNATURES[1], SIGNATURES[2])):
        face = compose_selection(sel)[0].resize((360, 360), Image.Resampling.LANCZOS)
        banner.alpha_composite(face, (70 + i * 460, 140))
    draw = ImageDraw.Draw(banner)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 72)
        small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 28)
    except OSError:
        font = ImageFont.load_default()
        small = font
    draw.text((64, 36), "INKLINGS", font=font, fill=(246, 239, 228, 255))
    draw.text((68, 112), "Smooth ink-wash PFP GIFs on Ink.", font=small, fill=(232, 200, 122, 255))
    banner.convert("RGB").save(BRAND_DIR / "banner-inklings.png", quality=94)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(gif_frames, BRAND_DIR / "collection-inklings.gif", DURATION_MS)

    (META_DIR / "inklings.json").write_text(
        json.dumps(
            {
                "name": "Inklings",
                "symbol": "INKL",
                "description": (
                    "Inklings is a 5,555-piece collection of illustrated PFP portraits. "
                    "Each face is stacked from painterly GIF layers — paper washes drift, blooms breathe, "
                    "visages bob, eyes blink — then flattened onto one shared 16-frame clock. "
                    "Soft edges only. Minting on Ink."
                ),
                "image": "/brand/collection-inklings.gif",
                "banner_image": "/brand/banner-inklings.png",
                "external_link": "/inklings",
                "seller_fee_basis_points": 500,
                "fee_recipient": "0x0000000000000000000000000000000000000000",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    print("Building Inklings ink-wash traits…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
