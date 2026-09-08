#!/usr/bin/env python3
"""Paint Cera — paraffin lava lamps.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
The portrait is a glass flask of oil on a nightstand. The wax is the loop.
Not cardboard matchbooks. Not snow globes. Not neon tubing. Not stamped tin.
Not origami. Not engraved busts. Not sticker cutouts. Not oval-egg bodies.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gif_bake import save_loop_gif  # noqa: E402
from paint_kit import DURATION_MS, FRAMES, SIZE, place_portrait, save_apng, save_image  # noqa: E402

GIF_COLORS = 128
GIF_DITHER = Image.Dither.NONE

TRAIT_DIR = ROOT / "public" / "cera-traits"
PREVIEW_DIR = ROOT / "public" / "cera-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

CX = 256.0
NECK_Y = 82.0
FLOOR_Y = 322.0
SOCKET_TOP = 308.0

NIGHT = (22, 18, 28, 255)
CHROME = (197, 200, 206)
GOLD = (212, 168, 72)
MAGENTA = (217, 70, 166)
INK = 8
RING = 6

SILL = {
    "wood": ((142, 92, 48), (92, 54, 28)),
    "formica": ((196, 186, 148), (88, 112, 64)),
    "velvet": ((48, 22, 42), (92, 36, 72)),
    "tile": ((214, 198, 176), (168, 92, 72)),
    "night": ((18, 16, 28), (42, 36, 62)),
}

SOCKET = {
    "rocket": (186, 188, 194),
    "saucer": (212, 168, 64),
    "cone": (88, 112, 64),
    "cube": (196, 72, 48),
    "mushroom": (148, 92, 168),
    "chrome": (210, 214, 220),
    "walnut": (92, 54, 32),
    "ceramic": (236, 228, 214),
}

SERUM = {
    "clear": (214, 226, 232),
    "cyan": (48, 176, 188),
    "amber": (212, 148, 48),
    "violet": (112, 72, 168),
    "green": (48, 148, 92),
}

MELT = {
    "crimson": (196, 36, 48),
    "gold": (236, 176, 36),
    "white": (236, 230, 220),
    "magenta": (208, 48, 148),
    "black": (36, 28, 32),
}

COIL = {
    "dim": (148, 72, 28),
    "orange": (255, 132, 36),
    "whitehot": (255, 236, 196),
}

LID = {
    "chrome": CHROME,
    "gold": GOLD,
    "painted": MAGENTA,
}


def clock(frame: int) -> float:
    return frame / FRAMES * math.pi * 2.0


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def inner_poly() -> list[tuple[int, int]]:
    """Shared liquid column every flask encloses."""
    cx = int(CX)
    return [
        (cx - 20, int(NECK_Y + 10)),
        (cx + 20, int(NECK_Y + 10)),
        (cx + 28, int(NECK_Y + 36)),
        (cx + 46, 210),
        (cx + 64, int(FLOOR_Y - 14)),
        (cx + 56, int(FLOOR_Y - 2)),
        (cx - 56, int(FLOOR_Y - 2)),
        (cx - 64, int(FLOOR_Y - 14)),
        (cx - 46, 210),
        (cx - 28, int(NECK_Y + 36)),
    ]


def flask_poly(kind: str) -> list[tuple[int, int]]:
    cx = int(CX)
    top = int(NECK_Y)
    bot = int(FLOOR_Y)
    if kind == "taper":
        return [
            (cx - 22, top),
            (cx + 22, top),
            (cx + 30, top + 32),
            (cx + 52, 208),
            (cx + 74, bot - 12),
            (cx + 66, bot),
            (cx - 66, bot),
            (cx - 74, bot - 12),
            (cx - 52, 208),
            (cx - 30, top + 32),
        ]
    if kind == "cylinder":
        return [
            (cx - 24, top),
            (cx + 24, top),
            (cx + 36, top + 18),
            (cx + 58, top + 36),
            (cx + 58, bot - 10),
            (cx + 50, bot),
            (cx - 50, bot),
            (cx - 58, bot - 10),
            (cx - 58, top + 36),
            (cx - 36, top + 18),
        ]
    if kind == "teardrop":
        return [
            (cx - 20, top),
            (cx + 20, top),
            (cx + 34, top + 40),
            (cx + 78, 200),
            (cx + 70, bot - 28),
            (cx + 42, bot),
            (cx - 42, bot),
            (cx - 70, bot - 28),
            (cx - 78, 200),
            (cx - 34, top + 40),
        ]
    # bulb — spherical body, short neck
    return [
        (cx - 18, top),
        (cx + 18, top),
        (cx + 28, top + 22),
        (cx + 82, 168),
        (cx + 88, 230),
        (cx + 62, bot - 8),
        (cx + 40, bot),
        (cx - 40, bot),
        (cx - 62, bot - 8),
        (cx - 88, 230),
        (cx - 82, 168),
        (cx - 28, top + 22),
    ]


def flask_mask(kind: str | None = None) -> Image.Image:
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).polygon(inner_poly() if kind is None else flask_poly(kind), fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.6))


def clip_to_inner(layer: Image.Image) -> Image.Image:
    out = layer.copy()
    out.putalpha(ImageChops.darker(layer.split()[-1], flask_mask()))
    return out


def paint_sill(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    a, b = SILL[kind]
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    if kind == "wood":
        grain = 14.0 * np.sin(yy / 7.5 + 0.35 * np.sin(xx / 40.0))
        for i in range(3):
            rgb[..., i] = a[i] + grain * (0.55 if i == 0 else 0.35)
        rgb[yy > 400] = np.array(b, dtype=np.float32)
    elif kind == "formica":
        for i in range(3):
            rgb[..., i] = a[i]
        boomer = np.sin((xx / 28.0) + np.cos(yy / 36.0) * 2.2) * np.sin((xx + yy) / 50.0)
        rgb[boomer > 0.35] = np.array(b, dtype=np.float32)
        kidney = ((xx - 380) ** 2 / 90 ** 2 + (yy - 120) ** 2 / 50 ** 2) < 1.0
        rgb[kidney] = np.array((196, 72, 96), dtype=np.float32)
    elif kind == "velvet":
        nap = 10.0 * np.sin(xx / 11.0) * np.sin(yy / 17.0)
        for i in range(3):
            rgb[..., i] = a[i] + nap
        rgb[yy > 430] = np.array(b, dtype=np.float32)
    elif kind == "tile":
        cell_x = (xx // 48).astype(np.int32)
        cell_y = (yy // 48).astype(np.int32)
        checker = ((cell_x + cell_y) % 2).astype(np.float32)
        for i in range(3):
            rgb[..., i] = a[i] * (1.0 - checker) + b[i] * checker
        grout = (np.abs(xx % 48 - 0) < 2) | (np.abs(yy % 48 - 0) < 2)
        rgb[grout] = np.array((92, 78, 70), dtype=np.float32)
    else:
        for i in range(3):
            rgb[..., i] = a[i] + 8.0 * np.sin((xx + yy) / 90.0)
        window = (xx > 360) & (xx < 490) & (yy > 40) & (yy < 210)
        rgb[window] = np.array(b, dtype=np.float32)
        pane = (np.abs(xx - 425) < 2) | (np.abs(yy - 125) < 2)
        rgb[window & pane] = np.array((18, 16, 28), dtype=np.float32)
    rgb += 3.0 * np.sin(yy / 80.0 + t * 0.05)[..., None]
    rng = np.random.RandomState(41)
    rgb += rng.randn(SIZE, SIZE, 1).astype(np.float32) * 2.2
    layer = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    shade = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(shade).ellipse((int(CX - 90), 350, int(CX + 100), 455), fill=(8, 6, 14, 90))
    layer.alpha_composite(shade.filter(ImageFilter.GaussianBlur(12)))
    return layer


def paint_socket(kind: str, frame: int) -> Image.Image:
    fill = SOCKET[kind]
    layer = blank()
    d = ImageDraw.Draw(layer)
    cx = int(CX)
    top = int(SOCKET_TOP)
    bot = 448
    dark = tuple(max(0, c - 40) for c in fill)
    lite = tuple(min(255, c + 36) for c in fill)

    if kind == "rocket":
        d.polygon(
            [(cx - 86, bot), (cx - 58, top + 18), (cx - 28, top), (cx + 28, top), (cx + 58, top + 18), (cx + 86, bot)],
            fill=fill + (255,),
        )
        d.polygon(
            [(cx - 86, bot), (cx - 58, top + 18), (cx - 28, top), (cx + 28, top), (cx + 58, top + 18), (cx + 86, bot)],
            outline=NIGHT[:3] + (255,),
            width=INK,
        )
        for y in (top + 22, top + 48, top + 78):
            d.arc((cx - 54, y, cx + 54, y + 18), 0, 180, fill=lite + (220,), width=4)
        d.ellipse((cx - 18, top - 8, cx + 18, top + 14), fill=CHROME + (255,), outline=NIGHT[:3] + (255,), width=RING)
    elif kind == "saucer":
        d.ellipse((cx - 110, top + 36, cx + 110, bot), fill=fill + (255,), outline=NIGHT[:3] + (255,), width=INK)
        d.ellipse((cx - 70, top + 18, cx + 70, top + 70), fill=lite + (255,), outline=dark + (255,), width=RING)
        d.rectangle((cx - 32, top - 4, cx + 32, top + 28), fill=CHROME + (255,), outline=NIGHT[:3] + (255,), width=RING)
    elif kind == "cone":
        d.polygon(
            [(cx - 92, bot), (cx - 26, top), (cx + 26, top), (cx + 92, bot)],
            fill=fill + (255,),
            outline=NIGHT[:3] + (255,),
            width=INK,
        )
        d.line([(cx - 40, top + 40), (cx + 40, top + 40)], fill=lite + (200,), width=4)
        d.ellipse((cx - 20, top - 6, cx + 20, top + 16), fill=dark + (255,), outline=NIGHT[:3] + (255,), width=RING)
    elif kind == "cube":
        d.rounded_rectangle((cx - 72, top, cx + 72, bot), radius=8, fill=fill + (255,), outline=NIGHT[:3] + (255,), width=INK)
        d.rectangle((cx - 72, top + 28, cx + 72, top + 36), fill=dark + (255,))
        d.rectangle((cx - 18, top + 70, cx + 18, top + 110), fill=lite + (220,))
        d.ellipse((cx - 8, top + 82, cx + 8, top + 98), fill=NIGHT)
    elif kind == "mushroom":
        d.ellipse((cx - 96, top + 20, cx + 96, bot + 8), fill=fill + (255,), outline=NIGHT[:3] + (255,), width=INK)
        d.ellipse((cx - 40, top - 8, cx + 40, top + 36), fill=lite + (255,), outline=dark + (255,), width=RING)
        d.arc((cx - 70, top + 40, cx + 70, top + 90), 200, 340, fill=lite + (180,), width=5)
    elif kind == "chrome":
        d.rounded_rectangle((cx - 48, top, cx + 48, bot - 10), radius=6, fill=fill + (255,), outline=NIGHT[:3] + (255,), width=INK)
        d.rectangle((cx - 48, top + 16, cx - 30, bot - 26), fill=(255, 255, 255, 90))
        d.ellipse((cx - 70, bot - 28, cx + 70, bot + 6), fill=dark + (255,), outline=NIGHT[:3] + (255,), width=RING)
        d.ellipse((cx - 22, top - 6, cx + 22, top + 16), fill=CHROME + (255,), outline=NIGHT[:3] + (255,), width=RING)
    elif kind == "walnut":
        d.polygon(
            [(cx - 78, bot), (cx - 50, top + 24), (cx - 22, top), (cx + 22, top), (cx + 50, top + 24), (cx + 78, bot)],
            fill=fill + (255,),
            outline=NIGHT[:3] + (255,),
            width=INK,
        )
        for y in range(top + 20, bot - 8, 16):
            d.arc((cx - 46, y, cx + 46, y + 14), 10, 170, fill=lite + (160,), width=RING)
    else:
        d.rounded_rectangle((cx - 64, top + 8, cx + 64, bot), radius=22, fill=fill + (255,), outline=NIGHT[:3] + (255,), width=INK)
        d.ellipse((cx - 28, top - 4, cx + 28, top + 28), fill=(255, 255, 255, 40))
        d.arc((cx - 40, top + 50, cx + 40, top + 90), 200, 340, fill=(255, 255, 255, 120), width=4)

    # contact ring under the flask
    d.ellipse((cx - 36, top - 10, cx + 36, top + 12), fill=CHROME + (240,), outline=NIGHT[:3] + (255,), width=RING)
    return layer


def paint_flask(kind: str, frame: int) -> Image.Image:
    layer = blank()
    d = ImageDraw.Draw(layer)
    poly = flask_poly(kind)
    glass = (226, 236, 242, 36)
    d.polygon(poly, fill=glass)
    d.polygon(poly, outline=NIGHT[:3] + (255,), width=INK + 4)
    d.polygon(poly, outline=(236, 244, 252, 230), width=3)
    # left specular strip
    cx = int(CX)
    d.line(
        [(cx - 38, int(NECK_Y + 24)), (cx - 52, 210), (cx - 58, int(FLOOR_Y - 20))],
        fill=(255, 255, 255, 160),
        width=7,
    )
    d.line(
        [(cx + 40, int(NECK_Y + 30)), (cx + 54, 220), (cx + 60, int(FLOOR_Y - 24))],
        fill=(180, 210, 230, 90),
        width=5,
    )
    # neck collar
    d.rounded_rectangle(
        (cx - 26, int(NECK_Y - 8), cx + 26, int(NECK_Y + 12)),
        radius=4,
        fill=CHROME + (255,),
        outline=NIGHT[:3] + (255,),
        width=RING,
    )
    return layer


def paint_serum(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    color = SERUM[kind]
    layer = blank()
    d = ImageDraw.Draw(layer)
    alpha = 118 if kind == "clear" else 150
    d.polygon(inner_poly(), fill=color + (alpha,))
    # meniscus
    cx = int(CX)
    d.ellipse((cx - 22, int(NECK_Y + 6), cx + 22, int(NECK_Y + 22)), fill=tuple(min(255, c + 30) for c in color) + (90,))
    # caustic pulse from the coil
    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    pulse = 0.62 + 0.28 * (0.5 + 0.5 * math.sin(t))
    gy = int(FLOOR_Y - 28)
    rad = int(40 + 10 * pulse)
    g.ellipse((cx - rad, gy - 18, cx + rad, int(FLOOR_Y + 4)), fill=(255, 180, 80, int(50 * pulse)))
    layer.alpha_composite(glow.filter(ImageFilter.GaussianBlur(8)))
    # glass grain in the liquid
    arr = np.array(layer, dtype=np.float32)
    rng = np.random.RandomState(73)
    streak = rng.randn(SIZE, SIZE).astype(np.float32) * 3.5
    alpha_ch = arr[..., 3]
    for i in range(3):
        arr[..., i] = np.where(alpha_ch > 0, arr[..., i] + streak, arr[..., i])
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    return clip_to_inner(out)


def blob_state(frame: int, index: int) -> tuple[float, float, float]:
    """Slow hover: each mass stays in a lane and drifts a little."""
    t = clock(frame)
    y0 = FLOOR_Y - 36
    y1 = NECK_Y + 56
    homes = (0.16, 0.38, 0.58, 0.78)
    amps = (8.0, 10.0, 9.0, 6.0)
    home = y0 + (y1 - y0) * homes[index]
    y = home + amps[index] * math.sin(t + index * 1.15)
    stretch = 1.02 + 0.05 * math.sin(t + index * 0.7)
    width = 1.0 + 0.04 * math.cos(t + index * 0.9)
    return y, stretch, width


def paint_melt(kind: str, frame: int) -> Image.Image:
    color = MELT[kind]
    lite = tuple(min(255, c + 50) for c in color)
    dark = tuple(max(0, c - 40) for c in color)
    layer = blank()
    d = ImageDraw.Draw(layer)
    cx = int(CX)
    sizes = ((38, 28), (30, 22), (24, 18), (20, 16))
    offsets = (-12, 16, -4, 10)
    for i, ((w, h), ox) in enumerate(zip(sizes, offsets)):
        y, stretch, width = blob_state(frame, i)
        ww = int(w * width)
        hh = int(h * stretch)
        x = cx + ox
        box = (x - ww, int(y - hh), x + ww, int(y + hh * 0.85))
        d.ellipse(box, fill=color + (230,), outline=dark + (220,), width=RING)
        # inner translucency
        d.ellipse(
            (box[0] + ww // 3, box[1] + hh // 4, box[2] - ww // 5, box[3] - hh // 3),
            fill=lite + (90,),
        )
        d.arc(box, 200, 320, fill=dark + (160,), width=RING)
    # puddle at the floor that feeds the rise
    puddle_h = 18 + int(2 * math.sin(clock(frame)))
    d.ellipse(
        (cx - 48, int(FLOOR_Y - 8 - puddle_h), cx + 48, int(FLOOR_Y + 2)),
        fill=color + (235,),
    )
    return clip_to_inner(layer.filter(ImageFilter.GaussianBlur(0.4)))


def paint_coil(kind: str, frame: int) -> Image.Image:
    color = COIL[kind]
    t = clock(frame)
    pulse = 0.78 + 0.18 * math.sin(t)
    layer = blank()
    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    cx = int(CX)
    y = int(FLOOR_Y - 16)
    rad = int(28 + 8 * pulse)
    alpha = {"dim": 70, "orange": 120, "whitehot": 160}[kind]
    g.ellipse((cx - rad, y - 16, cx + rad, y + 20), fill=color + (int(alpha * pulse),))
    layer.alpha_composite(glow.filter(ImageFilter.GaussianBlur(7)))
    d = ImageDraw.Draw(layer)
    # heating element — a short zigzag nest
    pts = []
    for i in range(7):
        pts.append((cx - 18 + i * 6, y - 4 + (4 if i % 2 else -4)))
    d.line(pts, fill=color + (255,), width=RING)
    d.ellipse((cx - 22, y - 2, cx + 22, y + 10), outline=tuple(max(0, c - 30) for c in color) + (200,), width=RING)
    return clip_to_inner(layer)


def paint_lid(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    fill = LID[kind]
    layer = blank()
    d = ImageDraw.Draw(layer)
    cx = int(CX)
    top = int(NECK_Y - 28)
    d.rounded_rectangle(
        (cx - 30, top, cx + 30, int(NECK_Y + 8)),
        radius=8,
        fill=fill + (255,),
        outline=NIGHT[:3] + (255,),
        width=INK,
    )
    d.ellipse((cx - 32, top - 8, cx + 32, top + 16), fill=tuple(min(255, c + 24) for c in fill) + (255,), outline=NIGHT[:3] + (255,), width=RING)
    d.arc((cx - 18, top - 4, cx + 18, top + 10), 200, 340, fill=(255, 255, 255, 140), width=3)
    if kind == "painted":
        d.ellipse((cx - 8, top, cx + 8, top + 10), fill=(255, 220, 80, 220))
    return layer


STACK = ("sill", "socket", "flask", "serum", "melt", "coil", "lid")

PAINTERS = {
    "sill": {k: (lambda kind: (lambda frame, k=kind: paint_sill(k, frame)))(k) for k in SILL},
    "socket": {k: (lambda kind: (lambda frame, k=kind: paint_socket(k, frame)))(k) for k in SOCKET},
    "flask": {k: (lambda kind: (lambda frame, k=kind: paint_flask(k, frame)))(k) for k in ("taper", "cylinder", "teardrop", "bulb")},
    "serum": {k: (lambda kind: (lambda frame, k=kind: paint_serum(k, frame)))(k) for k in SERUM},
    "melt": {k: (lambda kind: (lambda frame, k=kind: paint_melt(k, frame)))(k) for k in MELT},
    "coil": {k: (lambda kind: (lambda frame, k=kind: paint_coil(k, frame)))(k) for k in COIL},
    "lid": {k: (lambda kind: (lambda frame, k=kind: paint_lid(k, frame)))(k) for k in ("chrome", "gold", "painted", "none")},
}

TRAIT_SPEC: dict[str, list[tuple[str, str, int]]] = {
    "sill": [
        ("wood", "Wood Sill", 22),
        ("formica", "Formica Sill", 22),
        ("velvet", "Velvet Sill", 20),
        ("tile", "Tile Sill", 18),
        ("night", "Night Sill", 18),
    ],
    "socket": [
        ("rocket", "Rocket Socket", 16),
        ("saucer", "Saucer Socket", 14),
        ("cone", "Cone Socket", 14),
        ("cube", "Cube Socket", 12),
        ("mushroom", "Mushroom Socket", 12),
        ("chrome", "Chrome Socket", 12),
        ("walnut", "Walnut Socket", 10),
        ("ceramic", "Ceramic Socket", 10),
    ],
    "flask": [
        ("taper", "Taper Flask", 32),
        ("cylinder", "Cylinder Flask", 26),
        ("teardrop", "Teardrop Flask", 22),
        ("bulb", "Bulb Flask", 20),
    ],
    "serum": [
        ("clear", "Clear Serum", 24),
        ("cyan", "Cyan Serum", 22),
        ("amber", "Amber Serum", 20),
        ("violet", "Violet Serum", 18),
        ("green", "Green Serum", 16),
    ],
    "melt": [
        ("crimson", "Crimson Melt", 24),
        ("gold", "Gold Melt", 22),
        ("white", "White Melt", 20),
        ("magenta", "Magenta Melt", 18),
        ("black", "Black Melt", 16),
    ],
    "coil": [
        ("dim", "Dim Coil", 36),
        ("orange", "Orange Coil", 34),
        ("whitehot", "White-Hot Coil", 30),
    ],
    "lid": [
        ("none", "No Lid", 28),
        ("chrome", "Chrome Lid", 26),
        ("gold", "Gold Lid", 24),
        ("painted", "Painted Lid", 22),
    ],
}

SIGNATURES = [
    {"sill": "wood", "socket": "rocket", "flask": "taper", "serum": "cyan", "melt": "crimson", "coil": "orange", "lid": "chrome"},
    {"sill": "formica", "socket": "saucer", "flask": "cylinder", "serum": "amber", "melt": "gold", "coil": "dim", "lid": "none"},
    {"sill": "velvet", "socket": "cone", "flask": "teardrop", "serum": "violet", "melt": "magenta", "coil": "whitehot", "lid": "gold"},
    {"sill": "tile", "socket": "cube", "flask": "bulb", "serum": "green", "melt": "white", "coil": "orange", "lid": "painted"},
    {"sill": "night", "socket": "mushroom", "flask": "taper", "serum": "clear", "melt": "black", "coil": "dim", "lid": "chrome"},
    {"sill": "wood", "socket": "chrome", "flask": "cylinder", "serum": "cyan", "melt": "gold", "coil": "whitehot", "lid": "none"},
    {"sill": "formica", "socket": "walnut", "flask": "teardrop", "serum": "amber", "melt": "crimson", "coil": "orange", "lid": "gold"},
    {"sill": "velvet", "socket": "ceramic", "flask": "bulb", "serum": "violet", "melt": "white", "coil": "dim", "lid": "painted"},
    {"sill": "tile", "socket": "rocket", "flask": "cylinder", "serum": "green", "melt": "magenta", "coil": "whitehot", "lid": "chrome"},
    {"sill": "night", "socket": "saucer", "flask": "taper", "serum": "clear", "melt": "gold", "coil": "orange", "lid": "none"},
    {"sill": "wood", "socket": "cone", "flask": "bulb", "serum": "cyan", "melt": "black", "coil": "dim", "lid": "gold"},
    {"sill": "formica", "socket": "cube", "flask": "teardrop", "serum": "amber", "melt": "white", "coil": "orange", "lid": "painted"},
    {"sill": "velvet", "socket": "mushroom", "flask": "cylinder", "serum": "violet", "melt": "crimson", "coil": "whitehot", "lid": "chrome"},
    {"sill": "tile", "socket": "chrome", "flask": "taper", "serum": "green", "melt": "magenta", "coil": "dim", "lid": "none"},
    {"sill": "night", "socket": "walnut", "flask": "bulb", "serum": "clear", "melt": "gold", "coil": "orange", "lid": "gold"},
    {"sill": "wood", "socket": "ceramic", "flask": "teardrop", "serum": "cyan", "melt": "white", "coil": "whitehot", "lid": "painted"},
]

TRAIT_LABELS = (
    ("sill", "Sill"),
    ("socket", "Socket"),
    ("flask", "Flask"),
    ("serum", "Serum"),
    ("melt", "Melt"),
    ("coil", "Coil"),
    ("lid", "Lid"),
)

COLLECTION_DESCRIPTION = (
    "Cera is a 10,000-piece collection of looping lava-lamp PFP GIFs. "
    "Each lamp is stacked from seven plates — sill, socket, flask, serum, melt, coil, and lid — "
    "then flattened onto one 12-frame GIF. Paraffin in a glass flask on a nightstand. The wax is the loop."
)

COLLECTION_STORY = (
    "Cera.\n\n"
    "A 10,000-piece collection of looping lava-lamp PFP GIFs on Robinhood Chain. "
    "Each lamp is stacked from seven plates — sill, socket, flask, serum, melt, coil, and lid — "
    "then flattened onto one 12-frame GIF. Eight sockets: rocket, saucer, cone, cube, mushroom, chrome, walnut, and ceramic. "
    "The glass holds oil. The wax is the loop.\n\n"
    "A paraffin lamp on a nightstand, not a matchbook. Not a tin toy. Not a snow globe. Not neon tubing. "
    "No sticker edge. No egg. Not a shadow puppet. Not a fold. The flask stays seated on one envelope. "
    "The melt is the wax. One shared clock.\n\n"
    "Minting at $0.25 on Robinhood Chain (chain ID 4663). Gas is ETH."
)


def trait_path(category: str, trait_id: str) -> Path:
    return TRAIT_DIR / category / f"{trait_id}.png"


def render_trait_frames(category: str, trait_id: str) -> list[Image.Image]:
    paint = PAINTERS[category][trait_id]
    return [paint(frame) for frame in range(FRAMES)]


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


def build_traits(only: str | None = None, ids: list[str] | None = None) -> None:
    TRAIT_DIR.mkdir(parents=True, exist_ok=True)
    wanted = set(ids) if ids else None
    for category, traits in TRAIT_SPEC.items():
        if only and category != only:
            continue
        for trait_id, _name, _rarity in traits:
            if trait_id == "none":
                continue
            if wanted and trait_id not in wanted:
                continue
            print(f"  {category}/{trait_id}")
            save_apng(render_trait_frames(category, trait_id), trait_path(category, trait_id))
    manifest = {
        "name": "Cera",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Eight sockets share one flask column; the wax is the loop.",
    }
    (TRAIT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def build_samples() -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    samples = []
    for index, selection in enumerate(SIGNATURES, start=1):
        print(f"  sample #{index}")
        frames = compose_selection(selection)
        save_loop_gif(
            frames,
            PREVIEW_DIR / f"{index}.gif",
            DURATION_MS,
            colors=GIF_COLORS,
            dither=GIF_DITHER,
            palette_picks=FRAMES,
        )
        samples.append(
            {
                "id": index,
                "name": f"Lamp #{index}",
                "image": f"/cera-preview/{index}.gif",
                "attributes": [
                    {"trait_type": label, "value": name_of(key, selection[key])} for key, label in TRAIT_LABELS
                ],
            }
        )
    write_ts_gallery(samples)
    write_ts_traits()
    (PREVIEW_DIR / "samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")


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
            f'    image: "{sample["image"]}?v=3",\n'
            f"    attributes: [\n      {attrs},\n    ],\n"
            "  }"
        )
    (SRC_DATA / "cera-gallery.ts").write_text(
        "export type CeraSample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const ceraSamples: CeraSample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def write_ts_traits() -> None:
    blurbs = {
        "sill": "The nightstand — wood, formica, velvet, tile, night.",
        "socket": "The lamp foot — rocket, saucer, cone, cube, mushroom, chrome, walnut, ceramic.",
        "flask": "The glass — taper, cylinder, teardrop, bulb.",
        "serum": "The oil — clear, cyan, amber, violet, green.",
        "melt": "The paraffin — crimson, gold, white, magenta, black. The wax is the loop.",
        "coil": "The heater — dim, orange, white-hot.",
        "lid": "A chrome, gold, or painted cap.",
    }
    none_labels = {"lid": "No Lid"}
    cats = []
    for key, label in TRAIT_LABELS:
        traits = []
        for trait_id, name, rarity in TRAIT_SPEC[key]:
            if trait_id == "none":
                continue
            traits.append(
                "      { "
                f'id: "{trait_id}", name: "{name}", image: "/cera-traits/{key}/{trait_id}.png", rarity: {rarity} '
                "}"
            )
        none = none_labels.get(key)
        none_line = f'\n    noneLabel: "{none}",' if none else ""
        cats.append(
            "  {\n"
            f'    id: "{key}",\n'
            f'    label: "{label}",\n'
            f'    blurb: "{blurbs[key]}",'
            f"{none_line}\n"
            "    traits: [\n"
            + ",\n".join(traits)
            + ",\n    ],\n"
            "  }"
        )
    ids = " | ".join(f'"{key}"' for key, _label in TRAIT_LABELS)
    (SRC_DATA / "cera-traits.ts").write_text(
        "export type CeraTrait = {\n"
        "  id: string;\n"
        "  name: string;\n"
        "  image?: string;\n"
        "  rarity: number;\n"
        "};\n\n"
        "export type CeraTraitCategory = {\n"
        f"  id: {ids};\n"
        "  label: string;\n"
        "  blurb: string;\n"
        "  noneLabel?: string;\n"
        "  traits: CeraTrait[];\n"
        "};\n\n"
        "/** Bump when APNG layers change so the studio does not keep a stale loop. */\n"
        'export const CERA_ART_VERSION = "cera-v3";\n\n'
        "export const CERA_FRAMES = 12;\n"
        "export const CERA_DURATION_MS = 90;\n\n"
        "export function ceraTraitSrc(path?: string) {\n"
        "  if (!path) return \"\";\n"
        "  return `${path}?v=${CERA_ART_VERSION}`;\n"
        "}\n\n"
        "export const ceraTraitCategories: CeraTraitCategory[] = [\n"
        + ",\n".join(cats)
        + "\n];\n\n"
        'export const noneCeraTrait: CeraTrait = { id: "none", name: "None", rarity: 0 };\n\n'
        "export function ceraCategoryById(id: CeraTraitCategory[\"id\"]) {\n"
        "  const category = ceraTraitCategories.find((item) => item.id === id);\n"
        "  if (!category) throw new Error(`Unknown Cera trait category: ${id}`);\n"
        "  return category;\n"
        "}\n\n"
        "export function findCeraTrait(categoryId: CeraTraitCategory[\"id\"], traitId: string) {\n"
        "  if (traitId === \"none\") return noneCeraTrait;\n"
        "  return ceraCategoryById(categoryId).traits.find((trait) => trait.id === traitId);\n"
        "}\n\n"
        "export const defaultCeraSelection = {\n"
        '  sill: "wood",\n'
        '  socket: "rocket",\n'
        '  flask: "taper",\n'
        '  serum: "cyan",\n'
        '  melt: "crimson",\n'
        '  coil: "orange",\n'
        '  lid: "chrome",\n'
        "} as const;\n\n"
        "export type CeraSelection = Record<CeraTraitCategory[\"id\"], string>;\n\n"
        "export function randomCeraSelection(): CeraSelection {\n"
        "  const pick = (category: CeraTraitCategory) => {\n"
        "    const pool: CeraTrait[] = category.noneLabel\n"
        '      ? [{ id: "none", name: category.noneLabel, rarity: 22 }, ...category.traits]\n'
        "      : category.traits;\n"
        "    const total = pool.reduce((sum, trait) => sum + Math.max(trait.rarity, 1), 0);\n"
        "    let roll = Math.random() * total;\n"
        "    for (const trait of pool) {\n"
        "      roll -= Math.max(trait.rarity, 1);\n"
        "      if (roll <= 0) return trait.id;\n"
        "    }\n"
        "    return pool[0].id;\n"
        "  };\n\n"
        "  return {\n"
        '    sill: pick(ceraCategoryById("sill")),\n'
        '    socket: pick(ceraCategoryById("socket")),\n'
        '    flask: pick(ceraCategoryById("flask")),\n'
        '    serum: pick(ceraCategoryById("serum")),\n'
        '    melt: pick(ceraCategoryById("melt")),\n'
        '    coil: pick(ceraCategoryById("coil")),\n'
        '    lid: pick(ceraCategoryById("lid")),\n'
        "  };\n"
        "}\n\n"
        "export function ceraCombinationCount() {\n"
        "  return ceraTraitCategories.reduce((product, category) => {\n"
        "    const extra = category.noneLabel ? 1 : 0;\n"
        "    return product * (category.traits.length + extra);\n"
        "  }, 1);\n"
        "}\n\n"
        "export function ceraSelectionToLayers(selection: CeraSelection) {\n"
        '  return (["sill", "socket", "flask", "serum", "melt", "coil", "lid"] as const)\n'
        "    .map((id) => findCeraTrait(id, selection[id]))\n"
        "    .filter((trait): trait is CeraTrait => Boolean(trait?.image))\n"
        "    .map((trait) => ceraTraitSrc(trait.image));\n"
        "}\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array(
        [
            [0.09, 0.07, 0.11],
            [0.85, 0.27, 0.65],
            [0.19, 0.69, 0.74],
            [0.83, 0.66, 0.28],
        ],
        dtype=np.float32,
    )
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)
    yy = np.linspace(0.0, 1.0, height, dtype=np.float32)[:, None]
    xx = np.broadcast_to(x, (height, width))
    t = np.clip(xx * 0.55 + yy * 0.45, 0.0, 0.999) * (len(colors) - 1)
    i0 = np.floor(t).astype(np.int32)
    f = (t - i0)[..., None]
    rgb_out = colors[i0] * (1.0 - f) + colors[np.clip(i0 + 1, 0, len(colors) - 1)] * f
    arr = np.dstack([np.clip(rgb_out * 255.0, 0, 255).astype(np.uint8), np.full((height, width), 255, dtype=np.uint8)])
    return Image.fromarray(arr, "RGBA")


def write_collection_meta() -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    (META_DIR / "cera-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "cera.json").write_text(
        json.dumps(
            {
                "name": "Cera",
                "symbol": "CERA",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-cera.gif",
                "featured_image": "/brand/featured-cera.jpg",
                "banner_image": "/brand/banner-cera.png",
                "opensea_banner_image": "/brand/banner-cera-opensea.jpg",
                "external_link": "/cera",
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
    ImageDraw.Draw(mask).rounded_rectangle((16, 16, SIZE - 17, SIZE - 17), radius=36, fill=255)
    logo.putalpha(Image.composite(logo.split()[-1], Image.new("L", (SIZE, SIZE), 0), mask))
    rim = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(rim).rounded_rectangle(
        (12, 12, SIZE - 13, SIZE - 13), radius=40, outline=(217, 70, 166, 255), width=4
    )
    logo = Image.alpha_composite(logo, rim)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-cera.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-cera-loop.png",
    )

    def lineup(width: int, height: int, faces: list[Image.Image]) -> Image.Image:
        canvas = panoramic_wash(width, height)
        count = len(faces)
        size = int(height * 0.82)
        overlap = size // 5
        total = size * count - overlap * (count - 1)
        start_x = (width - total) // 2
        y = (height - size) // 2 + int(height * 0.03)
        for index, portrait in enumerate(faces):
            px = start_x + index * (size - overlap)
            place_portrait(canvas, portrait, px, y, size, radius=max(20, size // 16))
        return canvas

    save_image(lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-cera.png", quality=94)
    save_image(lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-cera-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=28)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=28)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-cera.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(
        gif_frames,
        BRAND_DIR / "collection-cera.gif",
        DURATION_MS,
        colors=GIF_COLORS,
        dither=GIF_DITHER,
        palette_picks=FRAMES,
    )
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Cera brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Cera lava lamps…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
