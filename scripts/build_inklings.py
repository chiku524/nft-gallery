#!/usr/bin/env python3
"""Paint Inklings — smooth ink-wash PFP layers for an OpenSea Drop on Ink.

Every trait is a 16-frame APNG on a shared 640 canvas and 90ms clock.
Character layers share one breathe so a stacked preview stays locked together.
Paper and bloom move on their own washes. Soft edges only — no pixel art.
"""

from __future__ import annotations

import json
import math
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

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


# --- visages: cartoon squids ------------------------------------------------

VISAGES = {
    "bobtail": {
        "body": "c46a32",
        "shade": "8a3e18",
        "belly": "f3d7b0",
        "blush": "e89a8a",
        "dark": "5a2e16",
        "accent": "e8a090",
    },
    "reef": {
        "body": "3aa090",
        "shade": "1e6a60",
        "belly": "c8f0e4",
        "blush": "f0a090",
        "dark": "143c38",
        "accent": "7edcc8",
    },
    "dumbo": {
        "body": "d478a0",
        "shade": "9a4870",
        "belly": "f8d0e0",
        "blush": "f090a8",
        "dark": "5a2840",
        "accent": "f0b0c8",
    },
    "cuttle": {
        "body": "6a7ab0",
        "shade": "3a4a78",
        "belly": "d8e0f0",
        "blush": "e8a0b0",
        "dark": "242848",
        "accent": "90a0d0",
    },
    "glass": {
        "body": "d8e8e8",
        "shade": "90a8b0",
        "belly": "f8fcfc",
        "blush": "e8c0c0",
        "dark": "5a7078",
        "accent": "c0d8d8",
    },
    "firefly": {
        "body": "3a2a68",
        "shade": "1e1840",
        "belly": "c8b8e8",
        "blush": "e890c0",
        "dark": "140c28",
        "accent": "e8c87a",
    },
    "giant": {
        "body": "8a5a3a",
        "shade": "5a3820",
        "belly": "f0e0c8",
        "blush": "d49078",
        "dark": "4a2e1e",
        "accent": "c89068",
    },
    "inked": {
        "body": "2a2438",
        "shade": "14101c",
        "belly": "6a6080",
        "blush": "c07090",
        "dark": "0c0814",
        "accent": "4a4060",
    },
}


def paint_arms(
    arr: np.ndarray,
    cx: float,
    cy: float,
    body: np.ndarray,
    shade: np.ndarray,
    belly: np.ndarray,
    sway: float,
    extra_len: float = 0.0,
    spread: float = 1.0,
    long_tentacles: bool = True,
) -> None:
    if long_tentacles:
        for sign in (-1.0, 1.0):
            tx = cx + sign * (78 + sway * 0.55)
            ty = cy + 168 + extra_len * 0.28
            ellipse(arr, tx, ty, 13, 92 + extra_len, body, 0.96, soft=11)
            ellipse(arr, tx + sign * 22, ty + 72 + extra_len * 0.15, 30, 20, body, 0.94, soft=10)
            disc(arr, tx + sign * 14, ty + 70, 8, belly, 0.55, soft=5)
            disc(arr, tx + sign * 24, ty + 78, 6.5, belly, 0.48, soft=5)
            disc(arr, tx + sign * 8, ty + 40, 5, shade, 0.28, soft=4)
    arms = (
        (-78, 0.28, 22, 38),
        (-56, 0.5, 16, 52),
        (-34, 0.78, 13, 64),
        (-12, 1.0, 12, 70),
        (12, 1.0, 12, 70),
        (34, 0.78, 13, 64),
        (56, 0.5, 16, 52),
        (78, 0.28, 22, 38),
    )
    for i, (ox, vert, rx, ry) in enumerate(arms):
        ox *= spread
        length = ry + extra_len * 0.16
        tx = cx + ox + sway * (0.4 if i % 2 == 0 else -0.4)
        ty = cy + 108 + length * 0.42 * vert
        ellipse(arr, tx, ty, rx, length * 0.5, body, 0.97, soft=10)
        disc(arr, tx, ty + length * 0.22 * vert, 6.5, belly, 0.55, soft=5)
        disc(arr, tx + (4 if ox > 0 else -4), ty + length * 0.08, 4.5, shade, 0.22, soft=4)


def paint_fins(
    arr: np.ndarray,
    cx: float,
    cy: float,
    body: np.ndarray,
    accent: np.ndarray,
    blush: np.ndarray,
    mx: float,
    kind: str,
) -> None:
    if kind == "dumbo":
        ellipse(arr, cx - 122, cy - 6, 76, 52, accent, 0.9, soft=16)
        ellipse(arr, cx + 122, cy - 6, 76, 52, accent, 0.9, soft=16)
        ellipse(arr, cx - 118, cy - 2, 36, 22, blush, 0.38, soft=12)
        ellipse(arr, cx + 118, cy - 2, 36, 22, blush, 0.38, soft=12)
        return
    if kind == "cuttle":
        ellipse(arr, cx, cy + 8, 188, 40, accent, 0.8, soft=18)
        ellipse(arr, cx, cy - 40, 158, 30, accent, 0.58, soft=16)
        return
    fy = cy - 42
    ellipse(arr, cx - mx * 0.95, fy, 52, 38, body, 0.96, soft=13)
    ellipse(arr, cx + mx * 0.95, fy, 52, 38, body, 0.96, soft=13)
    ellipse(arr, cx - mx * 1.08, fy - 8, 28, 22, accent, 0.4, soft=10)
    ellipse(arr, cx + mx * 1.08, fy - 8, 28, 22, accent, 0.4, soft=10)


def paint_visage(kind: str, frame: int) -> np.ndarray:
    palette = VISAGES[kind]
    body, shade, belly, blush, dark, accent = (
        rgb(palette[k]) for k in ("body", "shade", "belly", "blush", "dark", "accent")
    )
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    sway = math.sin(phase(frame)) * 7
    extra = 36.0 if kind == "reef" else (22.0 if kind == "giant" else 0.0)
    spread = 0.72 if kind == "bobtail" else (1.14 if kind == "giant" else 1.0)
    paint_arms(
        arr,
        cx,
        cy,
        body,
        shade,
        belly,
        sway,
        extra_len=extra,
        spread=spread,
        long_tentacles=kind != "bobtail",
    )

    mx, my = 120.0, 132.0
    if kind == "bobtail":
        mx, my = 128.0, 116.0
    elif kind == "giant":
        mx, my = 138.0, 146.0
    elif kind == "glass":
        mx, my = 114.0, 128.0
    elif kind == "cuttle":
        mx, my = 128.0, 118.0

    paint_fins(arr, cx, cy, body, accent, blush, mx, kind)

    mantle_opacity = 0.76 if kind == "glass" else 0.99
    ellipse(arr, cx, cy - 10, mx + 10, my + 8, shade, 0.42, soft=16)
    ellipse(arr, cx, cy - 14, mx, my, body, mantle_opacity, soft=15)
    ellipse(arr, cx, cy - my * 0.62, mx * 0.52, my * 0.42, body, mantle_opacity, soft=13)
    glow(arr, cx, cy + 16, 72, shade, 0.16)
    ellipse(arr, cx, cy + 38, mx * 0.56, my * 0.36, belly, 0.64 if kind != "glass" else 0.38, soft=16)
    disc(arr, cx - 72, cy + 28, 22, blush, 0.28, soft=14)
    disc(arr, cx + 72, cy + 28, 22, blush, 0.28, soft=14)
    ellipse(arr, cx + mx * 0.48, cy + 52, 20, 11, shade, 0.55, soft=8)
    ellipse(arr, cx, cy + 62, 16, 10, shade, 0.5, soft=7)
    ellipse(arr, cx, cy + 74, 20, 6, dark, 0.28, soft=5)

    if kind == "firefly":
        for i, (px, py, r) in enumerate(((-40, -58, 10), (36, -40, 8), (8, 20, 7), (-18, -12, 6))):
            pulse = 0.45 + 0.35 * math.sin(phase(frame) + i * 0.9)
            glow(arr, cx + px, cy + py, r * 2.2, accent, pulse)
            disc(arr, cx + px, cy + py, r, accent, 0.8, soft=6)
    elif kind == "inked":
        disc(arr, cx + 78, cy + 96, 36, dark, 0.48, soft=18)
        disc(arr, cx - 70, cy + 118, 24, dark, 0.34, soft=14)
        disc(arr, cx + 22, cy - 56, 18, accent, 0.35, soft=12)
    elif kind == "glass":
        glow(arr, cx - 24, cy - 48, 72, belly, 0.3)
        ellipse(arr, cx - 28, cy - 44, 36, 22, rgb("ffffff"), 0.24, soft=12)
    elif kind == "reef":
        ellipse(arr, cx - 32, cy - 64, 22, 16, accent, 0.48, soft=10)
        ellipse(arr, cx + 44, cy - 24, 18, 14, accent, 0.36, soft=10)
        disc(arr, cx - 8, cy - 20, 10, accent, 0.32, soft=8)
    return arr


# --- gaze -------------------------------------------------------------------

def paint_gaze(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    ly, ry = cx - 48, cx + 48
    ey = cy + 4
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
        ry_eye = 28.0 * max(open_amt, 0.08)
        if shut >= 0.92:
            ellipse(arr, ex, ey, 30, 5, lid, 0.78, soft=5)
            return
        ellipse(arr, ex, ey, 32, ry_eye, sclera, 0.98, soft=6)
        iris_y = ey + (3 if kind == "lidded" else 0)
        ellipse(arr, ex, iris_y, 18, 18 * open_amt, iris, 0.97, soft=5)
        ellipse(arr, ex, iris_y, 9, 9 * open_amt, pupil, 0.95, soft=3)
        if kind == "ember":
            glow(arr, ex, iris_y, 22, rgb("ff8a50"), 0.38 * open_amt)
        disc(arr, ex - 6, ey - 8 * open_amt, 5.2, shine, 0.9 * open_amt, soft=3)
        disc(arr, ex + 8, ey + 4 * open_amt, 2.4, shine, 0.55 * open_amt, soft=2)
        if kind == "dew":
            disc(arr, ex + 6, ey + 6 * open_amt, 2.6, shine, 0.7 * open_amt, soft=2)
            disc(arr, ex, ey + 22, 3.4, rgb("c8d8e8"), 0.35 * open_amt, soft=4)
        if kind in ("lidded", "sleepy"):
            ellipse(arr, ex, ey - ry_eye * 0.72, 32, 9, lid, 0.3, soft=6)

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
        kelp = rgb("1e3a32")
        shine = rgb("4a8a72")
        ellipse(arr, cx - 118 + sway * 0.4, cy + 8, 28, 150, kelp, 0.82, soft=16)
        ellipse(arr, cx + 118 + sway * 0.4, cy + 8, 28, 150, kelp, 0.82, soft=16)
        ellipse(arr, cx - 96 + sway * 0.25, cy + 40, 18, 120, kelp, 0.7, soft=14)
        ellipse(arr, cx + 96 + sway * 0.25, cy + 40, 18, 120, kelp, 0.7, soft=14)
        disc(arr, cx - 118, cy - 40, 10, shine, 0.28, soft=8)
        disc(arr, cx + 118, cy - 20, 8, shine, 0.22, soft=7)
    elif kind == "bun":
        pearl = rgb("f4efe6")
        gold = rgb("e8c87a")
        disc(arr, cx, cy - 142, 22, pearl, 0.95, soft=8)
        disc(arr, cx - 22, cy - 128, 16, pearl, 0.9, soft=7)
        disc(arr, cx + 22, cy - 128, 16, pearl, 0.9, soft=7)
        disc(arr, cx, cy - 148, 7, gold, 0.7, soft=4)
        disc(arr, cx - 6, cy - 146, 5, rgb("ffffff"), 0.55, soft=3)
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
        ("bobtail", "Bobtail", 16),
        ("reef", "Reef", 14),
        ("dumbo", "Dumbo", 14),
        ("cuttle", "Cuttle", 14),
        ("glass", "Glass", 12),
        ("firefly", "Firefly", 12),
        ("giant", "Giant", 10),
        ("inked", "Inked", 8),
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
        ("none", "Clean mantle", 34),
        ("splash", "Ink Splash", 16),
        ("drip", "Slow Drip", 14),
        ("seal", "Red Seal", 12),
        ("streak", "Brush Streak", 12),
    ],
    "adorn": [
        ("none", "Bare mantle", 22),
        ("flow", "Kelp Flow", 16),
        ("bun", "Pearl Cluster", 14),
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
    {"paper": "indigo", "bloom": "violet", "visage": "bobtail", "gaze": "bright", "mark": "none", "adorn": "flow"},
    {"paper": "peach", "bloom": "gold", "visage": "reef", "gaze": "lidded", "mark": "seal", "adorn": "bun"},
    {"paper": "celadon", "bloom": "teal", "visage": "dumbo", "gaze": "dew", "mark": "splash", "adorn": "none"},
    {"paper": "charcoal", "bloom": "none", "visage": "cuttle", "gaze": "wink", "mark": "drip", "adorn": "ribbon"},
    {"paper": "rose", "bloom": "coral", "visage": "glass", "gaze": "ember", "mark": "none", "adorn": "hood"},
    {"paper": "storm", "bloom": "silver", "visage": "firefly", "gaze": "sleepy", "mark": "streak", "adorn": "crown"},
    {"paper": "wine", "bloom": "gold", "visage": "giant", "gaze": "bright", "mark": "seal", "adorn": "flow"},
    {"paper": "cream", "bloom": "violet", "visage": "inked", "gaze": "dew", "mark": "none", "adorn": "bun"},
    {"paper": "indigo", "bloom": "silver", "visage": "reef", "gaze": "ember", "mark": "streak", "adorn": "hood"},
    {"paper": "peach", "bloom": "coral", "visage": "bobtail", "gaze": "wink", "mark": "splash", "adorn": "crown"},
    {"paper": "celadon", "bloom": "none", "visage": "giant", "gaze": "lidded", "mark": "none", "adorn": "ribbon"},
    {"paper": "charcoal", "bloom": "violet", "visage": "glass", "gaze": "bright", "mark": "drip", "adorn": "flow"},
    {"paper": "rose", "bloom": "gold", "visage": "firefly", "gaze": "dew", "mark": "seal", "adorn": "none"},
    {"paper": "storm", "bloom": "teal", "visage": "cuttle", "gaze": "sleepy", "mark": "none", "adorn": "bun"},
    {"paper": "wine", "bloom": "coral", "visage": "inked", "gaze": "ember", "mark": "splash", "adorn": "hood"},
    {"paper": "cream", "bloom": "gold", "visage": "dumbo", "gaze": "bright", "mark": "streak", "adorn": "crown"},
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


COLLECTION_DESCRIPTION = (
    "Inklings is a 5,555-piece collection of looping cartoon-squid PFPs on Ink. "
    "Each squid is stacked from six painterly layers — paper, bloom, visage, gaze, mark, and adorn — "
    "then flattened onto one 16-frame GIF. Washes drift, eyes blink, tentacles sway. Nothing is pixelated."
)

COLLECTION_STORY = (
    "Inklings are painted cartoon squids, not pixel art.\n\n"
    "A 5,555-piece collection of looping ink-wash squid PFPs on Ink, Kraken’s Ethereum layer 2. "
    "Each Inkling is stacked from six painterly layers — paper, bloom, visage, gaze, mark, and adorn — "
    "then flattened onto one 16-frame GIF. Dye drifts. Eyes blink. Tentacles sway. Soft edges only.\n\n"
    "Minting on Ink (chain ID 57073). Gas is ETH. 0.006 ETH to mint."
)


def panoramic_wash(width: int, height: int, frame: int = 0) -> Image.Image:
    left = np.asarray(to_image(paint_paper("indigo", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    mid = np.asarray(to_image(paint_paper("peach", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    right = np.asarray(to_image(paint_paper("celadon", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
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
    ImageDraw.Draw(shadow).rounded_rectangle((8, 14, size + 8, size + 18), radius=radius, fill=(10, 6, 18, 90))
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
    (META_DIR / "inklings-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "inklings.json").write_text(
        json.dumps(
            {
                "name": "Inklings",
                "symbol": "INKL",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-inklings.gif",
                "featured_image": "/brand/featured-inklings.jpg",
                "banner_image": "/brand/banner-inklings.png",
                "opensea_banner_image": "/brand/banner-inklings-opensea.jpg",
                "external_link": "/inklings",
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
    ImageDraw.Draw(ring).ellipse((10, 10, SIZE - 10, SIZE - 10), outline=(232, 200, 122, 220), width=10)
    logo = Image.alpha_composite(logo, ring)
    logo.resize((512, 512), Image.Resampling.LANCZOS).save(BRAND_DIR / "logo-inklings.png")
    save_apng([frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames], BRAND_DIR / "logo-inklings-loop.png")

    site_banner = lineup_banner(1500, 560, portraits[:5])
    site_banner.convert("RGB").save(BRAND_DIR / "banner-inklings.png", quality=94)

    opensea_banner = lineup_banner(2800, 700, portraits)
    opensea_banner.convert("RGB").save(BRAND_DIR / "banner-inklings-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800, frame=8)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=64)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=64)
    featured.convert("RGB").save(BRAND_DIR / "featured-inklings.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(gif_frames, BRAND_DIR / "collection-inklings.gif", DURATION_MS)
    write_collection_meta()



def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true", help="Rebuild logo, banners, and listing copy")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Inklings brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Inklings ink-wash traits…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
