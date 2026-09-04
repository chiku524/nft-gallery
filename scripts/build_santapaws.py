#!/usr/bin/env python3
"""Paint Santa Paws — looping chibi-cat PFP layers for an OpenSea Drop on Base.

Sibling to Purrkins (kawaii bust-crop cats, thick outlines, flat cel fills)
with a giving / Christmas / cozy-winter wardrobe. Every trait is a 12-frame
APNG on a shared 512 canvas and 90ms clock (same clock as Foxins).

Pelt, mug, hat, and gear share one bob so a stacked preview stays locked.
Yard stays put. Glow pulses on its own loop.
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

from build_purrkins import (  # noqa: E402
    BUST_RX,
    BUST_RY,
    BUST_Y,
    FRAMES,
    H,
    HEAD,
    HEAD_RX,
    HEAD_RY,
    LINE,
    SIZE,
    W,
    blink_amount,
    bob,
    disc,
    ellipse,
    fill_poly,
    glow,
    grain,
    halo_ring,
    lite,
    mix_scalar,
    outlined_disc,
    outlined_ear,
    outlined_ellipse,
    outlined_roundrect,
    phase,
    place_portrait,
    rgb,
    rounded_rect,
    save_image,
    shade,
    to_image,
    write_bytes_retry,
)
from gif_bake import save_loop_gif  # noqa: E402

TRAIT_DIR = ROOT / "public" / "santapaws-traits"
PREVIEW_DIR = ROOT / "public" / "santapaws-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

DURATION_MS = 90

SANTA = rgb("c43b3b")
PINE = rgb("2f6a4a")
GOLD = rgb("f0c45a")
CREAM = rgb("fff6e8")
INK = LINE
HOLLY = rgb("1e5a38")
COCOA = rgb("5a3a24")
SNOW = rgb("f4f7fb")


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


def blank() -> np.ndarray:
    return np.zeros((H, W, 4), dtype=np.float32)


# --- yard -------------------------------------------------------------------

YARDS = {
    "snowy": ("12203a", "0a1428", 7),
    "hearth": ("5a2a1c", "2a1410", 11),
    "candy": ("f4e8e8", "e8d0d4", 13),
    "wrap": ("1e4632", "143024", 17),
    "aurora": ("102430", "1a1838", 19),
    "kitchen": ("f3ead8", "e4d0b4", 23),
}


def paint_yard(kind: str, frame: int) -> np.ndarray:
    top_h, bot_h, seed = YARDS[kind]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    t = phase(frame)
    top, bot = rgb(top_h), rgb(bot_h)
    v = yy / (H - 1)
    wash = top * (1.0 - (v * 0.88 + 0.06 * math.sin(t))[..., None]) + bot * (v * 0.88 + 0.06 * math.sin(t))[..., None]
    arr = blank()
    arr[..., :3] = wash
    arr[..., 3] = 1.0
    arr[..., :3] = np.clip(arr[..., :3] + grain(seed, 0.02)[..., None], 0.0, 1.0)

    if kind == "snowy":
        outlined_disc(arr, 420, 78, 28, rgb("fff4d8"), rgb("e8d8a8"), width=2.4, cel=False)
        glow(arr, 420, 78, 52, rgb("ffe8b0"), 0.22)
        for i in range(18):
            px = float((53 * i + 18 + int(frame * 7)) % W)
            py = float((29 * i + 12 + int(frame * 11)) % H)
            disc(arr, px, py, 2.4 + (i % 3) * 0.6, SNOW, 0.55 + 0.25 * math.sin(t + i), soft=1.1)
        glow(arr, 256, 80, 140, rgb("8ab4e8"), 0.10 + 0.03 * math.sin(t))
    elif kind == "hearth":
        glow(arr, 256, 470, 180, rgb("ff8a3a"), 0.28 + 0.08 * math.sin(t))
        rounded_rect(arr, 256, 490, 210, 36, shade(bot, 0.08), 0.7, radius=8)
        for i, px in enumerate((196.0, 256.0, 316.0)):
            disc(arr, px, 454 + math.sin(t + i) * 4, 16, rgb("ffb060"), 0.55, soft=2.4)
            disc(arr, px, 448 + math.sin(t * 1.4 + i) * 3, 8, rgb("ffe08a"), 0.7, soft=1.8)
        for i in range(7):
            px = 160 + i * 32
            py = 70 + (i % 3) * 18
            disc(arr, px, py, 2.0, GOLD, 0.35 + 0.2 * math.sin(t + i), soft=1.0)
    elif kind == "candy":
        stripe = ((xx + yy * 0.35 + frame * 4) / 28) % 2.0
        red = rgb("d44a4a")
        white = rgb("fff6f0")
        mask = (stripe < 1.0).astype(np.float32)
        arr[..., :3] = red * mask[..., None] + white * (1.0 - mask)[..., None]
        arr[..., 3] = 1.0
        glow(arr, 256, 200, 160, rgb("ffe0e8"), 0.12)
    elif kind == "wrap":
        for i in range(6):
            gy = 40 + i * 86
            rounded_rect(arr, 256, gy, 280, 4, GOLD, 0.22 + 0.06 * math.sin(t + i), radius=2)
        rounded_rect(arr, 256, 256, 22, 280, SANTA, 0.55, radius=6)
        rounded_rect(arr, 256, 256, 280, 22, SANTA, 0.55, radius=6)
        for i in range(8):
            ang = t * 0.3 + i * 0.8
            disc(arr, 80 + (i * 53) % 360, 70 + (i * 41) % 380, 5, GOLD, 0.45, soft=1.4)
        glow(arr, 256, 256, 90, GOLD, 0.14 + 0.04 * math.sin(t))
    elif kind == "aurora":
        for i, color in enumerate((rgb("4cffb0"), rgb("7a9cff"), rgb("e090ff"))):
            gy = 90 + i * 70 + math.sin(t + i) * 10
            ellipse(arr, 256 + math.sin(t * 0.6 + i) * 30, gy, 240, 28, color, 0.18 + 0.06 * math.sin(t + i), soft=8.0)
        for i in range(12):
            px = float((41 * i + 30) % W)
            py = float((17 * i + 10) % 180)
            disc(arr, px, py, 1.8, SNOW, 0.5 + 0.3 * math.sin(t + i), soft=1.0)
    else:
        rounded_rect(arr, 256, 86, 220, 10, shade(bot, 0.12), 0.35, radius=4)
        for i, (px, py) in enumerate(((90, 70), (160, 68), (230, 72), (300, 66), (370, 70), (430, 68))):
            disc(arr, px, py + math.sin(t + i) * 2, 9, rgb("d4a060"), 0.85, soft=1.6)
            disc(arr, px, py - 2 + math.sin(t + i) * 2, 4, rgb("8a5a2a"), 0.7, soft=1.2)
        rounded_rect(arr, 256, 478, 240, 44, shade(bot, 0.1), 0.45, radius=10)
        glow(arr, 400, 120, 50, rgb("fff0d0"), 0.18)
    return arr


# --- glow -------------------------------------------------------------------

GLOWS = {
    "halo": "ffe08a",
    "sparkle": "fff0b0",
    "glitter": "e8f4ff",
    "ember": "ff8a4a",
}


def paint_glow(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    t = phase(frame)
    color = rgb(GLOWS[kind])
    cx, cy = HEAD
    ring_rx = HEAD_RX + 62
    ring_ry = HEAD_RY + 52
    pulse = 0.36 + 0.08 * math.sin(t)
    halo_ring(arr, cx, cy, ring_rx, ring_ry, color, pulse * 0.78, stamp=44.0, count=20, spin=t * 0.1)
    glow(arr, cx, cy - HEAD_RY - 48, 88, color, pulse * 0.58)

    if kind == "sparkle":
        for i in range(12):
            ang = t + i * 0.52
            orbit = 1.02 + 0.1 * math.sin(t * 1.3 + i)
            disc(
                arr,
                cx + math.cos(ang) * ring_rx * orbit,
                cy + math.sin(ang) * ring_ry * orbit,
                3.6,
                color,
                0.76,
                soft=1.2,
            )
    elif kind == "glitter":
        for i in range(16):
            px = cx + math.cos(t * 0.8 + i) * (ring_rx + 8 + (i % 5) * 6)
            py = cy + math.sin(t * 0.9 + i * 0.7) * (ring_ry + 4) - (frame * 3 + i * 9) % 40
            disc(arr, px, py, 2.4, color, 0.7, soft=1.1)
    elif kind == "ember":
        glow(arr, cx, cy + HEAD_RY + 36, 80, color, pulse * 0.55)
        for i in range(6):
            disc(
                arr,
                cx + math.sin(t + i) * 70,
                cy + HEAD_RY + 10 - abs(math.sin(t * 1.2 + i)) * 18,
                5.0,
                color,
                0.5,
                soft=1.8,
            )
    else:
        halo_ring(arr, cx, cy, ring_rx + 16, ring_ry + 12, color, pulse * 0.36, stamp=26.0, count=14, spin=-t * 0.06)
    return arr


# --- pelt -------------------------------------------------------------------

PELTS = {
    "fluff": {
        "fur": "f6f1ea",
        "mark": "d4c8bc",
        "inner": "f2b4ac",
        "belly": "fffaf4",
        "nose": "2a221c",
        "stripes": False,
    },
    "ginger": {
        "fur": "e89a48",
        "mark": "c07028",
        "inner": "f0a898",
        "belly": "f8d8b0",
        "nose": "3a2214",
        "stripes": True,
    },
    "tuxedo": {
        "fur": "2a2a32",
        "mark": "1a1a22",
        "inner": "c08090",
        "belly": "f6f1ea",
        "nose": "121218",
        "stripes": False,
        "blaze": True,
    },
    "tabby": {
        "fur": "9aa0a6",
        "mark": "6e747a",
        "inner": "e8b4ac",
        "belly": "e8e4e0",
        "nose": "2a2624",
        "stripes": True,
    },
    "calico": {
        "fur": "f2ebe0",
        "mark": "e09040",
        "inner": "f0b0a8",
        "belly": "fff8f0",
        "nose": "2c2018",
        "stripes": False,
        "patch": True,
    },
    "charcoal": {
        "fur": "3a3a42",
        "mark": "222228",
        "inner": "c08090",
        "belly": "5a5a64",
        "nose": "121218",
        "stripes": False,
    },
    "cocoa": {
        "fur": "8a5a38",
        "mark": "5a3818",
        "inner": "e8a898",
        "belly": "d8b090",
        "nose": "2a1810",
        "stripes": False,
    },
}


def paint_pelt(kind: str, frame: int) -> np.ndarray:
    palette = PELTS[kind]
    fur, mark, inner, belly, nose = (rgb(palette[k]) for k in ("fur", "mark", "inner", "belly", "nose"))
    arr = blank()
    dy = bob(frame)
    cx, cy = HEAD[0], HEAD[1] + dy
    t = phase(frame)
    twitch = math.sin(t * 2) * 2.4
    rx, ry = HEAD_RX, HEAD_RY
    soot = rgb("2c2c34")
    ginger = rgb("e09040")

    outlined_ellipse(arr, cx, BUST_Y, BUST_RX - 8, BUST_RY - 4, fur, width=3.8)
    ellipse(arr, cx, 486, 42, 32, belly, 0.9, soft=2.4)

    left_tip = (cx - rx * 0.70, cy - ry - 44 + twitch)
    left_out = (cx - rx * 0.98, cy - ry + 56)
    left_in = (cx - rx * 0.24, cy - ry + 18)
    right_tip = (cx + rx * 0.70, cy - ry - 44 - twitch * 0.55)
    right_in = (cx + rx * 0.24, cy - ry + 18)
    right_out = (cx + rx * 0.98, cy - ry + 56)

    outlined_ear(arr, left_tip[0], left_tip[1], left_out, left_in, fur, inner)
    outlined_ear(arr, right_tip[0], right_tip[1], right_in, right_out, fur, inner)

    if kind == "calico":
        fill_poly(
            arr,
            [
                left_tip,
                (mix_scalar(left_tip[0], left_out[0], 0.55), mix_scalar(left_tip[1], left_out[1], 0.55)),
                (mix_scalar(left_tip[0], left_in[0], 0.55), mix_scalar(left_tip[1], left_in[1], 0.55)),
            ],
            soot,
            0.94,
        )

    outlined_ellipse(arr, cx, cy, rx, ry, fur, width=4.6)

    if kind == "tuxedo":
        ellipse(arr, cx, cy + ry * 0.10, rx * 0.38, ry * 0.46, belly, 0.96, soft=2.6)
        ellipse(arr, cx, cy - ry * 0.08, rx * 0.22, ry * 0.20, belly, 0.9, soft=2.4)
        fill_poly(
            arr,
            [
                (cx - 10, cy - ry * 0.02),
                (cx, cy + ry * 0.36),
                (cx + 10, cy - ry * 0.02),
            ],
            belly,
            0.92,
        )
    elif kind == "charcoal":
        ellipse(arr, cx, cy + ry * 0.08, rx * 0.34, ry * 0.38, belly, 0.82, soft=2.8)
    elif kind == "calico":
        ellipse(arr, cx + rx * 0.38, cy - ry * 0.32, rx * 0.30, ry * 0.26, ginger, 0.94, soft=2.2)
        ellipse(arr, cx + rx * 0.46, cy - ry * 0.04, rx * 0.18, ry * 0.16, ginger, 0.88, soft=2.0)
        ellipse(arr, cx - rx * 0.42, cy + ry * 0.30, rx * 0.18, ry * 0.14, soot, 0.9, soft=2.0)
        ellipse(arr, cx + 28, 488, 26, 20, ginger, 0.85, soft=2.0)
    elif kind == "fluff":
        ellipse(arr, cx - rx * 0.48, cy - ry * 0.04, 24, 18, mark, 0.2, soft=2.4)
        ellipse(arr, cx + rx * 0.48, cy - ry * 0.04, 24, 18, mark, 0.2, soft=2.4)
    elif kind == "cocoa":
        ellipse(arr, cx, cy - ry * 0.36, 26, 16, mark, 0.4, soft=2.0)

    if palette.get("stripes"):
        top = cy - ry * 0.46
        fill_poly(
            arr,
            [
                (cx - 32, top),
                (cx - 20, top + 36),
                (cx - 9, top + 16),
                (cx, top + 38),
                (cx + 9, top + 16),
                (cx + 20, top + 36),
                (cx + 32, top),
                (cx + 18, top),
                (cx + 11, top + 16),
                (cx, top + 24),
                (cx - 11, top + 16),
                (cx - 18, top),
            ],
            mark,
            0.82,
        )
        for side in (-1.0, 1.0):
            rounded_rect(arr, cx + side * rx * 0.54, cy + ry * 0.22, 17, 5.4, mark, 0.68, radius=3, soft=1.3)
            rounded_rect(arr, cx + side * rx * 0.50, cy + ry * 0.32, 14, 4.6, mark, 0.5, radius=3, soft=1.3)

    ellipse(arr, cx, cy + ry * 0.14, 40, 30, belly, 0.55, soft=2.8)
    disc(arr, cx - rx * 0.44, cy + ry * 0.20, 17, inner, 0.4, soft=3.0)
    disc(arr, cx + rx * 0.44, cy + ry * 0.20, 17, inner, 0.4, soft=3.0)
    outlined_ellipse(arr, cx, cy + ry * 0.18, 8.4, 6.0, nose, width=1.6, cel=False)
    disc(arr, cx - 2.4, cy + ry * 0.16, 2.0, rgb("ffffff"), 0.55, soft=1.0)
    return arr


# --- mug --------------------------------------------------------------------

def paint_mug(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    t = phase(frame)
    closed = blink_amount(frame)
    ink = LINE
    shine = rgb("fff8e8")
    pink = rgb("ff5a88")
    gold = rgb("ffe060")

    def eye(ex: float, ey: float, shut: float, heart: bool = False, spark: bool = False, wide: bool = False) -> None:
        r = 10.0 if wide else 8.6
        if shut >= 0.9:
            ellipse(arr, ex, ey + 2, r + 3, 2.6, ink, 0.96, soft=1.2)
            return
        if heart:
            disc(arr, ex, ey + 1.2, 7.0, pink, 0.98, soft=1.3)
            disc(arr, ex - 3.6, ey - 1.4, 4.0, pink, 0.95, soft=1.2)
            disc(arr, ex + 3.6, ey - 1.4, 4.0, pink, 0.95, soft=1.2)
            disc(arr, ex - 2.2, ey - 2.6, 1.6, shine, 0.85, soft=0.8)
        elif spark:
            disc(arr, ex, ey + 0.8, 7.0, gold, 0.98, soft=1.3)
            disc(arr, ex, ey + 0.8, 3.0, ink, 0.95, soft=1.0)
            disc(arr, ex - 2.2, ey - 2.0, 1.8, shine, 0.9, soft=0.8)
        else:
            disc(arr, ex, ey + 1.0, r, ink, 0.98, soft=1.2)
            disc(arr, ex - 2.0, ey - 1.6, 2.0, shine, 0.9, soft=0.8)
        if shut > 0.35:
            ellipse(arr, ex, ey - 5, r + 2, 5.5 * shut, ink, 0.88, soft=1.3)

    lx, rx, ey = cx - HEAD_RX * 0.30, cx + HEAD_RX * 0.30, cy + HEAD_RY * 0.04

    if kind == "wink":
        eye(lx, ey, 0.0)
        eye(rx, ey, 1.0)
    elif kind == "sleepy":
        eye(lx, ey + 2, 0.62)
        eye(rx, ey + 2, 0.62)
    elif kind == "surprise":
        eye(lx, ey - 1, closed, wide=True)
        eye(rx, ey - 1, closed, wide=True)
    elif kind == "heart":
        eye(lx, ey, closed, heart=True)
        eye(rx, ey, closed, heart=True)
    elif kind == "cheerful":
        eye(lx, ey, closed, spark=True)
        eye(rx, ey, closed, spark=True)
    else:
        eye(lx, ey, closed)
        eye(rx, ey, closed)

    my = cy + HEAD_RY * 0.34
    if kind == "sleepy":
        ellipse(arr, cx, my, 9, 1.8, ink, 0.8, soft=1.2)
    elif kind == "cheerful":
        ellipse(arr, cx, my + 3, 14, 2.6, ink, 0.9, soft=1.3)
    elif kind == "surprise":
        ellipse(arr, cx, my + 2, 6.5, 4.2, ink, 0.88, soft=1.2)
    elif kind == "tongue":
        ellipse(arr, cx, my + 2, 8, 2.0, ink, 0.88, soft=1.1)
        outlined_ellipse(arr, cx + 5, my + 10, 6.2, 7.4, rgb("ff7a90"), width=1.6, cel=False)
    elif kind == "blush":
        ellipse(arr, cx - 5.2, my, 5.0, 2.0, ink, 0.9, soft=1.1)
        ellipse(arr, cx + 5.2, my, 5.0, 2.0, ink, 0.9, soft=1.1)
        disc(arr, cx - HEAD_RX * 0.42, cy + HEAD_RY * 0.22, 16, pink, 0.42, soft=3.2)
        disc(arr, cx + HEAD_RX * 0.42, cy + HEAD_RY * 0.22, 16, pink, 0.42, soft=3.2)
    else:
        ellipse(arr, cx - 5.2, my, 5.0, 2.0, ink, 0.9, soft=1.1)
        ellipse(arr, cx + 5.2, my, 5.0, 2.0, ink, 0.9, soft=1.1)

    for side in (-1, 1):
        ellipse(arr, cx + side * HEAD_RX * 0.50, cy + HEAD_RY * 0.20, 15, 1.3, ink, 0.42, soft=1.1)
        ellipse(arr, cx + side * HEAD_RX * 0.48, cy + HEAD_RY * 0.26, 13, 1.15, ink, 0.32, soft=1.1)

    if kind == "cheerful":
        disc(arr, cx + HEAD_RX * 0.46, cy - HEAD_RY * 0.30, 3, gold, 0.7 + 0.2 * math.sin(t), soft=1.2)
    return arr


# --- hat --------------------------------------------------------------------

def paint_hat(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    t = phase(frame)
    rx, ry = HEAD_RX, HEAD_RY
    brim_y = cy - ry + 36

    if kind == "santa":
        fill_poly(
            arr,
            [
                (cx - rx * 0.62, brim_y + 4),
                (cx + rx * 0.18, cy - ry - 78),
                (cx + rx * 0.78, cy - ry - 8),
                (cx + rx * 0.58, brim_y + 10),
            ],
            SANTA,
        )
        fill_poly(
            arr,
            [
                (cx - rx * 0.66, brim_y - 2),
                (cx + rx * 0.16, cy - ry - 86),
                (cx + rx * 0.10, cy - ry - 70),
                (cx - rx * 0.50, brim_y + 6),
            ],
            INK,
            0.55,
        )
        outlined_ellipse(arr, cx + 6, brim_y + 8, rx * 0.78, 18, CREAM, width=3.2, cel=False)
        outlined_disc(arr, cx + rx * 0.72, cy - ry - 4 + math.sin(t) * 2, 16, CREAM, width=2.6, cel=False)
    elif kind == "elf":
        fill_poly(
            arr,
            [
                (cx - rx * 0.48, brim_y + 6),
                (cx + 8, cy - ry - 92),
                (cx + rx * 0.42, brim_y + 8),
            ],
            PINE,
        )
        outlined_ellipse(arr, cx, brim_y + 10, rx * 0.70, 16, GOLD, width=3.0, cel=False)
        outlined_disc(arr, cx + 10, cy - ry - 88 + math.sin(t) * 2, 12, GOLD, width=2.4, cel=False)
        for i, px in enumerate((cx - 36, cx - 8, cx + 22)):
            rounded_rect(arr, px, brim_y - 10 - i * 8, 5, 10, GOLD, 0.9, radius=2)
    elif kind == "antlers":
        for side in (-1.0, 1.0):
            base_x = cx + side * rx * 0.42
            tip_y = cy - ry - 70
            fill_poly(
                arr,
                [
                    (base_x - side * 8, cy - ry + 8),
                    (base_x + side * 6, cy - ry + 8),
                    (base_x + side * 18, tip_y),
                    (base_x + side * 4, tip_y + 8),
                ],
                COCOA,
            )
            fill_poly(
                arr,
                [
                    (base_x + side * 6, cy - ry - 28),
                    (base_x + side * 34, cy - ry - 48),
                    (base_x + side * 14, cy - ry - 22),
                ],
                COCOA,
            )
            fill_poly(
                arr,
                [
                    (base_x + side * 4, cy - ry - 46),
                    (base_x + side * 28, cy - ry - 68),
                    (base_x + side * 8, cy - ry - 40),
                ],
                COCOA,
            )
        disc(arr, cx - rx * 0.42, cy - ry + 6, 5, rgb("3a2414"), 0.9)
        disc(arr, cx + rx * 0.42, cy - ry + 6, 5, rgb("3a2414"), 0.9)
    elif kind == "beanie":
        outlined_ellipse(arr, cx, cy - ry + 22, rx * 0.70, 44, SANTA, width=3.4, cel=False)
        rounded_rect(arr, cx, cy - ry + 48, rx * 0.74, 16, CREAM, 0.98, radius=8)
        outlined_disc(arr, cx + 4, cy - ry - 16 + math.sin(t) * 1.5, 16, CREAM, width=2.6, cel=False)
    else:
        for i, ang in enumerate((-0.9, -0.2, 0.55)):
            lx = cx + math.cos(ang) * 28
            ly = cy - ry + 8 + math.sin(ang) * 10
            fill_poly(
                arr,
                [
                    (lx, ly - 22),
                    (lx - 16, ly + 10),
                    (lx + 16, ly + 10),
                ],
                HOLLY,
            )
        for px, py in ((cx - 10, cy - ry + 14), (cx + 4, cy - ry + 10), (cx + 14, cy - ry + 18)):
            outlined_disc(arr, px, py, 5.5, SANTA, width=1.8, cel=False)
    return arr


# --- gear -------------------------------------------------------------------

def paint_gear(kind: str, frame: int) -> np.ndarray:
    arr = blank()
    cx, cy = HEAD[0], HEAD[1] + bob(frame)
    t = phase(frame)
    sway = math.sin(t) * 2.2
    rx, ry = HEAD_RX, HEAD_RY
    neck = cy + ry + 4
    body_y = BUST_Y + bob(frame)

    if kind == "scarf":
        outlined_ellipse(arr, cx, neck + 6, 78, 16, SANTA, width=3.2, cel=False)
        fill_poly(
            arr,
            [
                (cx + 36, neck + 4),
                (cx + 78, neck + 70),
                (cx + 54, neck + 78),
                (cx + 22, neck + 14),
            ],
            PINE,
        )
        for i in range(4):
            rounded_rect(arr, cx - 40 + i * 28, neck + 6, 8, 5, CREAM, 0.85, radius=2)
    elif kind == "sweater":
        outlined_ellipse(arr, cx, body_y, BUST_RX, BUST_RY, SANTA, width=3.8, cel=False)
        ellipse(arr, cx, neck - 2, 62, 14, shade(SANTA, 0.12), 0.95, soft=2.0)
        for i, y in enumerate((456.0, 474.0, 492.0)):
            rounded_rect(arr, cx, y, 70, 4, CREAM, 0.7, radius=2)
        fill_poly(
            arr,
            [(cx, 448), (cx - 12, 468), (cx + 12, 468)],
            CREAM,
            0.85,
        )
    elif kind == "bells":
        outlined_ellipse(arr, cx, neck + 4, 64, 12, GOLD, width=3.0, cel=False)
        for px in (cx - 22, cx, cx + 22):
            outlined_disc(arr, px, neck + 22 + math.sin(t + px) * 1.5, 9, GOLD, width=2.2, cel=False)
            disc(arr, px, neck + 28 + math.sin(t + px) * 1.5, 2.2, COCOA, 0.9)
    elif kind == "cocoa":
        outlined_roundrect(arr, cx - 88 + sway, 480, 16, 22, CREAM, radius=6, width=3.0)
        rounded_rect(arr, cx - 88 + sway, 462, 18, 6, SANTA, 0.95, radius=3)
        ellipse(arr, cx - 88 + sway, 474, 11, 4.5, COCOA, 0.9, soft=1.4)
        rounded_rect(arr, cx - 70 + sway, 480, 3, 9, INK, 0.85, radius=2)
        steam = 0.45 + 0.2 * math.sin(t)
        ellipse(arr, cx - 94 + sway, 444, 4, 10, rgb("e8f0ff"), steam, soft=2.2)
        ellipse(arr, cx - 82 + sway, 438, 3.5, 9, rgb("e8f0ff"), steam * 0.8, soft=2.0)
    elif kind == "present":
        outlined_roundrect(arr, cx + 92 + sway, 478, 22, 20, rgb("2f6a4a"), radius=6, width=3.0)
        rounded_rect(arr, cx + 92 + sway, 478, 22, 5, SANTA, 0.95, radius=2)
        rounded_rect(arr, cx + 92 + sway, 478, 5, 20, SANTA, 0.95, radius=2)
        outlined_disc(arr, cx + 92 + sway, 454, 7, GOLD, width=2.0, cel=False)
    elif kind == "mistletoe":
        for i, (dx, dy) in enumerate(((-10, -6), (10, -4), (0, 8))):
            ellipse(arr, cx + dx, cy - ry - 8 + dy, 14, 8, HOLLY, 0.92, soft=1.6)
        for px, py in ((cx - 4, cy - ry + 4), (cx + 6, cy - ry + 2), (cx + 1, cy - ry + 12)):
            outlined_disc(arr, px, py, 4.2, SANTA, width=1.6, cel=False)
        ellipse(arr, cx, cy - ry - 22, 3, 10, HOLLY, 0.8, soft=1.2)
    else:
        outlined_roundrect(arr, cx + 96 + sway, 470, 14, 28, SANTA, radius=8, width=3.0)
        rounded_rect(arr, cx + 96 + sway, 444, 18, 8, CREAM, 0.95, radius=3)
        disc(arr, cx + 96 + sway, 488, 5, CREAM, 0.9)
        for i in range(3):
            disc(arr, cx + 88 + sway + i * 8, 456, 2.2, PINE, 0.85)
    return arr


# --- catalog ----------------------------------------------------------------

TRAIT_SPEC = {
    "yard": [
        ("snowy", "Snowy Night", 22),
        ("hearth", "Cozy Hearth", 20),
        ("candy", "Candy Cane", 16),
        ("wrap", "Gift Wrap", 14),
        ("kitchen", "Cookie Kitchen", 14),
        ("aurora", "Aurora", 14),
    ],
    "glow": [
        ("none", "No glow", 28),
        ("halo", "Soft Halo", 20),
        ("sparkle", "Sparkle", 18),
        ("glitter", "Snow Glitter", 18),
        ("ember", "Ember", 16),
    ],
    "pelt": [
        ("fluff", "White Fluff", 20),
        ("ginger", "Ginger", 18),
        ("tuxedo", "Tuxedo", 16),
        ("tabby", "Gray Tabby", 16),
        ("calico", "Calico", 12),
        ("charcoal", "Charcoal", 10),
        ("cocoa", "Cocoa", 8),
    ],
    "mug": [
        ("cheerful", "Cheerful", 20),
        ("wink", "Wink", 16),
        ("sleepy", "Sleepy", 16),
        ("blush", "Blush", 14),
        ("surprise", "Surprised", 12),
        ("tongue", "Tongue Out", 12),
        ("heart", "Heart Eyes", 10),
    ],
    "hat": [
        ("none", "None", 22),
        ("santa", "Santa Hat", 22),
        ("elf", "Elf Cap", 16),
        ("beanie", "Pom Beanie", 14),
        ("antlers", "Antlers", 14),
        ("holly", "Holly Crown", 12),
    ],
    "gear": [
        ("none", "None", 18),
        ("scarf", "Scarf", 16),
        ("sweater", "Sweater", 14),
        ("bells", "Bells", 14),
        ("cocoa", "Cocoa", 12),
        ("present", "Present", 12),
        ("stocking", "Stocking", 8),
        ("mistletoe", "Mistletoe", 6),
    ],
}

PAINTERS = {
    "yard": {k: (lambda kind: (lambda frame, k=kind: paint_yard(k, frame)))(k) for k in YARDS},
    "glow": {k: (lambda kind: (lambda frame, k=kind: paint_glow(k, frame)))(k) for k in GLOWS},
    "pelt": {k: (lambda kind: (lambda frame, k=kind: paint_pelt(k, frame)))(k) for k in PELTS},
    "mug": {
        k: (lambda kind: (lambda frame, k=kind: paint_mug(k, frame)))(k)
        for k in ("cheerful", "wink", "sleepy", "blush", "surprise", "tongue", "heart")
    },
    "hat": {
        k: (lambda kind: (lambda frame, k=kind: paint_hat(k, frame)))(k)
        for k in ("santa", "elf", "antlers", "beanie", "holly")
    },
    "gear": {
        k: (lambda kind: (lambda frame, k=kind: paint_gear(k, frame)))(k)
        for k in ("scarf", "sweater", "bells", "cocoa", "present", "mistletoe", "stocking")
    },
}

STACK = ("yard", "glow", "pelt", "mug", "hat", "gear")

SIGNATURES = [
    {"yard": "snowy", "glow": "halo", "pelt": "fluff", "mug": "cheerful", "hat": "santa", "gear": "scarf"},
    {"yard": "hearth", "glow": "ember", "pelt": "ginger", "mug": "wink", "hat": "beanie", "gear": "cocoa"},
    {"yard": "candy", "glow": "sparkle", "pelt": "calico", "mug": "heart", "hat": "elf", "gear": "present"},
    {"yard": "wrap", "glow": "glitter", "pelt": "tuxedo", "mug": "sleepy", "hat": "holly", "gear": "none"},
    {"yard": "aurora", "glow": "halo", "pelt": "charcoal", "mug": "surprise", "hat": "antlers", "gear": "bells"},
    {"yard": "kitchen", "glow": "none", "pelt": "cocoa", "mug": "tongue", "hat": "none", "gear": "stocking"},
    {"yard": "snowy", "glow": "glitter", "pelt": "tabby", "mug": "blush", "hat": "santa", "gear": "sweater"},
    {"yard": "hearth", "glow": "sparkle", "pelt": "fluff", "mug": "cheerful", "hat": "elf", "gear": "mistletoe"},
    {"yard": "candy", "glow": "none", "pelt": "ginger", "mug": "wink", "hat": "none", "gear": "scarf"},
    {"yard": "wrap", "glow": "ember", "pelt": "calico", "mug": "sleepy", "hat": "beanie", "gear": "cocoa"},
    {"yard": "aurora", "glow": "sparkle", "pelt": "tuxedo", "mug": "heart", "hat": "holly", "gear": "present"},
    {"yard": "kitchen", "glow": "halo", "pelt": "tabby", "mug": "cheerful", "hat": "antlers", "gear": "bells"},
    {"yard": "snowy", "glow": "ember", "pelt": "cocoa", "mug": "blush", "hat": "santa", "gear": "none"},
    {"yard": "hearth", "glow": "glitter", "pelt": "charcoal", "mug": "tongue", "hat": "none", "gear": "sweater"},
    {"yard": "candy", "glow": "halo", "pelt": "fluff", "mug": "surprise", "hat": "elf", "gear": "stocking"},
    {"yard": "aurora", "glow": "none", "pelt": "ginger", "mug": "wink", "hat": "holly", "gear": "mistletoe"},
]

TRAIT_LABELS = (
    ("yard", "Yard"),
    ("glow", "Glow"),
    ("pelt", "Pelt"),
    ("mug", "Mug"),
    ("hat", "Hat"),
    ("gear", "Gear"),
)

COLLECTION_DESCRIPTION = (
    "Santa Paws is a 7,777-piece collection of looping chibi-cat PFP GIFs on Base. "
    "Each cat is stacked from six layers — yard, glow, pelt, mug, hat, and gear — "
    "then flattened onto one 12-frame GIF. Thick outlines. Cozy winter yards. "
    "Always in the mood of giving."
)

COLLECTION_STORY = (
    "Santa Paws is always in the mood of giving.\n\n"
    "A 7,777-piece collection of looping chibi-cat PFP GIFs on Base. "
    "Each Santa Paw is stacked from six layers — yard, glow, pelt, mug, hat, and gear — "
    "then flattened onto one 12-frame GIF. Snowy nights and cookie kitchens behind them. "
    "Santa hats and cocoa on top. Ears twitch. Eyes blink. Soft bob.\n\n"
    "Kawaii bust-crop cats with thick outlines, flat cel fills, and a Christmas wardrobe. "
    "One shared clock.\n\n"
    "Minting on Base (chain ID 8453). Gas is ETH."
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
        "name": "Santa Paws",
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
                "name": f"Santa Paw #{index}",
                "image": f"/santapaws-preview/{index}.gif",
                "attributes": [
                    {"trait_type": label, "value": name_of(key, selection[key])} for key, label in TRAIT_LABELS
                ],
            }
        )
    (META_DIR / "santapaws-samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")
    write_ts_gallery(samples)


def write_ts_gallery(samples: list[dict]) -> None:
    SRC_DATA.mkdir(parents=True, exist_ok=True)
    rows = []
    for sample in samples:
        attrs = ",\n      ".join(
            f'{{ trait_type: "{a["trait_type"]}", value: "{a["value"]}" }}' for a in sample["attributes"]
        )
        rows.append(
            "  {\n"
            f"    id: {sample['id']},\n"
            f'    name: "{sample["name"]}",\n'
            f'    image: "{sample["image"]}",\n'
            f"    attributes: [\n      {attrs},\n    ],\n"
            "  }"
        )
    (SRC_DATA / "santapaw-gallery.ts").write_text(
        "export type SantaPawSample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const santapawSamples: SantaPawSample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int, frame: int = 0) -> Image.Image:
    left = np.asarray(to_image(paint_yard("snowy", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    mid = np.asarray(to_image(paint_yard("hearth", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    right = np.asarray(to_image(paint_yard("aurora", frame)).resize((width, height), Image.Resampling.LANCZOS), dtype=np.float32)
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)[None, :, None]
    w_left = np.clip(1.0 - x / 0.42, 0.0, 1.0)
    w_right = np.clip((x - 0.58) / 0.42, 0.0, 1.0)
    w_mid = np.clip(1.0 - w_left - w_right, 0.0, 1.0)
    out = left * w_left + mid * w_mid + right * w_right
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")


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
    (META_DIR / "santapaws-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "santapaws.json").write_text(
        json.dumps(
            {
                "name": "Santa Paws",
                "symbol": "PAWS",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-santapaws.gif",
                "featured_image": "/brand/featured-santapaws.jpg",
                "banner_image": "/brand/banner-santapaws.png",
                "opensea_banner_image": "/brand/banner-santapaws-opensea.jpg",
                "external_link": "/santapaws",
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
    ImageDraw.Draw(ring).ellipse((10, 10, SIZE - 10, SIZE - 10), outline=(196, 59, 59, 230), width=10)
    logo = Image.alpha_composite(logo, ring)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-santapaws.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-santapaws-loop.png",
    )

    save_image(lineup_banner(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-santapaws.png", quality=94)
    save_image(lineup_banner(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-santapaws-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800, frame=8)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=64)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=64)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-santapaws.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(gif_frames, BRAND_DIR / "collection-santapaws.gif", DURATION_MS)
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true", help="Rebuild logo, banners, and listing copy")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Santa Paws brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Santa Paws trait loops…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
