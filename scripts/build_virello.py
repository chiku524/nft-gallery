#!/usr/bin/env python3
"""Paint Virello — lithographed wind-up tin toys.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
The portrait is stamped metal on a toy-shop bench. The winding key is the loop.
Not a snow globe. Not neon tubing. Not leather puppets. Not origami facets.
Not engraved busts. Not sticker cutouts. Not oval-egg bodies. Not a dancer.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gif_bake import save_loop_gif  # noqa: E402
from paint_kit import DURATION_MS, FRAMES, SIZE, place_portrait, save_apng, save_image  # noqa: E402

GIF_COLORS = 128
GIF_DITHER = Image.Dither.NONE

TRAIT_DIR = ROOT / "public" / "virello-traits"
PREVIEW_DIR = ROOT / "public" / "virello-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

CX = 256.0
CY = 232.0
AXLE = (CX + 104.0, CY + 6.0)

INK = (32, 24, 20, 255)
TIN = (188, 184, 176, 255)
TIN_DARK = (132, 126, 118, 255)
PRINT_C = (36, 92, 118, 80)
PRINT_M = (148, 36, 64, 80)

BENCH = {
    "linoleum": ((214, 196, 164), (168, 72, 58)),
    "felt": ((46, 92, 64), (28, 58, 42)),
    "crate": ((156, 118, 72), (98, 68, 42)),
    "enamel": ((236, 232, 220), (48, 46, 44)),
    "pine": ((186, 148, 92), (128, 92, 52)),
}

ENAMEL = {
    "tomato": (196, 58, 42),
    "navy": (32, 58, 102),
    "mustard": (196, 148, 42),
    "chrome": (154, 168, 178),
    "mint": (72, 148, 118),
    "cream": (232, 214, 176),
    "cherry": (148, 36, 54),
}


def clock(frame: int) -> float:
    return frame / FRAMES * math.pi * 2.0


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def tap(frame: int) -> int:
    return int(round(math.sin(clock(frame) * 2.0) * 1.2))


def rot(px: float, py: float, ang: float, ox: float, oy: float) -> tuple[int, int]:
    dx, dy = px - ox, py - oy
    c, s = math.cos(ang), math.sin(ang)
    return int(round(ox + dx * c - dy * s)), int(round(oy + dx * s + dy * c))


def print_poly(d: ImageDraw.ImageDraw, pts: list[tuple[int, int]], fill, outline=True) -> None:
    d.polygon(pts, fill=fill)
    if outline:
        shifted_c = [(x + 1, y) for x, y in pts]
        shifted_m = [(x - 1, y) for x, y in pts]
        d.line(shifted_c + [shifted_c[0]], fill=PRINT_C, width=2)
        d.line(shifted_m + [shifted_m[0]], fill=PRINT_M, width=2)
        d.line(pts + [pts[0]], fill=INK, width=3)


def print_ellipse(d: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill, width: int = 3) -> None:
    d.ellipse(box, fill=fill)
    x0, y0, x1, y1 = box
    d.ellipse((x0 + 1, y0, x1 + 1, y1), outline=PRINT_C, width=max(1, width - 1))
    d.ellipse((x0 - 1, y0, x1 - 1, y1), outline=PRINT_M, width=max(1, width - 1))
    d.ellipse(box, outline=INK, width=width)


def print_rect(d: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill, radius: int = 0) -> None:
    if radius:
        d.rounded_rectangle(box, radius=radius, fill=fill)
        d.rounded_rectangle((box[0] + 1, box[1], box[2] + 1, box[3]), radius=radius, outline=PRINT_C, width=2)
        d.rounded_rectangle((box[0] - 1, box[1], box[2] - 1, box[3]), radius=radius, outline=PRINT_M, width=2)
        d.rounded_rectangle(box, radius=radius, outline=INK, width=3)
    else:
        d.rectangle(box, fill=fill)
        d.rectangle((box[0] + 1, box[1], box[2] + 1, box[3]), outline=PRINT_C, width=2)
        d.rectangle((box[0] - 1, box[1], box[2] - 1, box[3]), outline=PRINT_M, width=2)
        d.rectangle(box, outline=INK, width=3)


def tab_row(d: ImageDraw.ImageDraw, y: int, x0: int, x1: int) -> None:
    x = x0 + 8
    while x < x1 - 10:
        d.rounded_rectangle((x, y - 3, x + 12, y + 8), radius=3, fill=TIN_DARK)
        d.rectangle((x + 3, y + 1, x + 9, y + 5), fill=INK[:3] + (180,))
        x += 18


def wheel(d: ImageDraw.ImageDraw, cx: int, cy: int, r: int = 22) -> None:
    print_ellipse(d, (cx - r, cy - r, cx + r, cy + r), TIN_DARK)
    d.ellipse((cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8), fill=(72, 68, 62, 255))
    d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=INK)


def paint_bench(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    top, accent = BENCH[kind]
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    wall = np.array([236.0, 226.0, 206.0])
    dado = np.array(accent, dtype=np.float32)
    speck = 6.0 * np.sin(xx / 7.0) * np.sin(yy / 9.0)
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    rail = (yy > 210) & (yy < 248)
    floor = yy >= 338
    for i in range(3):
        rgb[..., i] = wall[i] + speck * 0.35
        rgb[..., i] = np.where(rail, dado[i] * 0.92 + speck * 0.2, rgb[..., i])
        rgb[..., i] = np.where(floor, top[i] + speck * 0.8, rgb[..., i])
    rgb += 3.0 * np.sin(yy / 90.0 + t * 0.05)[..., None]
    layer = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    d = ImageDraw.Draw(layer)
    if kind == "linoleum":
        for i in range(0, SIZE, 28):
            d.line([(0, 338 + (i % 56)), (SIZE, 338 + (i % 56))], fill=accent + (40,), width=1)
    elif kind == "felt":
        d.rectangle((0, 338, SIZE, SIZE), fill=top + (255,))
        d.ellipse((int(CX - 90), 350, int(CX + 90), 410), fill=(20, 40, 28, 40))
    elif kind == "crate":
        for i in range(6):
            y = 338 + i * 28
            d.rectangle((0, y, SIZE, y + 22), fill=(top[0] - i * 6, top[1] - i * 4, top[2] - i * 3, 255))
            d.line([(0, y + 22), (SIZE, y + 22)], fill=INK[:3] + (80,), width=2)
    elif kind == "enamel":
        d.rectangle((18, 330, SIZE - 18, SIZE - 12), fill=top + (255,))
        d.rectangle((18, 330, SIZE - 18, SIZE - 12), outline=accent + (255,), width=6)
    else:
        for i in range(8):
            x = i * 64
            d.rectangle((x, 338, x + 58, SIZE), fill=(top[0] - (i % 2) * 18, top[1] - (i % 2) * 12, top[2] - 8, 255))
            d.line([(x + 58, 338), (x + 58, SIZE)], fill=INK[:3] + (70,), width=2)
    shade = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(shade).ellipse((int(CX - 120), 348, int(CX + 130), 412), fill=(20, 14, 10, 70))
    layer.alpha_composite(shade.filter(ImageFilter.GaussianBlur(8)))
    return layer


def paint_chassis(kind: str, frame: int) -> Image.Image:
    layer = blank()
    d = ImageDraw.Draw(layer)
    dy = tap(frame)
    y = int(CY + dy)

    if kind == "robot":
        print_rect(d, (int(CX - 52), y - 18, int(CX + 52), y + 78), TIN, radius=8)
        print_ellipse(d, (int(CX - 36), y - 96, int(CX + 36), y - 16), TIN)
        d.rectangle((int(CX - 4), y - 112, int(CX + 4), y - 90), fill=TIN_DARK)
        d.ellipse((int(CX - 8), y - 122, int(CX + 8), y - 106), fill=INK)
        d.rectangle((int(CX - 18), y - 72, int(CX - 6), y - 58), fill=INK)
        d.rectangle((int(CX + 6), y - 72, int(CX + 18), y - 58), fill=INK)
        print_rect(d, (int(CX - 78), y - 8, int(CX - 50), y + 42), TIN, radius=4)
        print_rect(d, (int(CX + 50), y - 8, int(CX + 78), y + 42), TIN, radius=4)
        print_rect(d, (int(CX - 44), y + 76, int(CX - 14), y + 118), TIN_DARK, radius=4)
        print_rect(d, (int(CX + 14), y + 76, int(CX + 44), y + 118), TIN_DARK, radius=4)
        tab_row(d, y + 78, int(CX - 48), int(CX + 48))
        wheel(d, int(CX - 30), y + 126, 16)
        wheel(d, int(CX + 30), y + 126, 16)
    elif kind == "duck":
        print_ellipse(d, (int(CX - 78), y - 18, int(CX + 64), y + 86), TIN)
        print_ellipse(d, (int(CX + 20), y - 70, int(CX + 86), y + 8), TIN)
        print_poly(d, [(int(CX + 78), y - 28), (int(CX + 124), y - 8), (int(CX + 78), y + 8)], TIN)
        d.ellipse((int(CX + 48), y - 52, int(CX + 62), y - 38), fill=INK)
        print_ellipse(d, (int(CX - 20), y - 8, int(CX + 36), y + 36), TIN_DARK)
        tab_row(d, y + 84, int(CX - 60), int(CX + 40))
        wheel(d, int(CX - 36), y + 108, 20)
        wheel(d, int(CX + 28), y + 108, 20)
    elif kind == "racer":
        print_poly(
            d,
            [
                (int(CX - 100), y + 28),
                (int(CX - 70), y - 8),
                (int(CX + 40), y - 18),
                (int(CX + 96), y + 12),
                (int(CX + 88), y + 52),
                (int(CX - 92), y + 56),
            ],
            TIN,
        )
        print_ellipse(d, (int(CX - 18), y - 36, int(CX + 38), y + 18), TIN_DARK)
        d.polygon(
            [(int(CX + 40), y - 16), (int(CX + 86), y - 28), (int(CX + 90), y - 8), (int(CX + 48), y + 4)],
            fill=TIN_DARK,
        )
        tab_row(d, y + 54, int(CX - 80), int(CX + 70))
        wheel(d, int(CX - 62), y + 78, 24)
        wheel(d, int(CX + 58), y + 78, 24)
    elif kind == "soldier":
        print_rect(d, (int(CX - 34), y - 20, int(CX + 34), y + 70), TIN, radius=4)
        print_ellipse(d, (int(CX - 28), y - 86, int(CX + 28), y - 18), TIN)
        d.rectangle((int(CX - 22), y - 96, int(CX + 22), y - 72), fill=TIN_DARK)
        d.rectangle((int(CX - 10), y - 64, int(CX - 2), y - 52), fill=INK)
        d.rectangle((int(CX + 4), y - 64, int(CX + 12), y - 52), fill=INK)
        print_rect(d, (int(CX - 54), y - 8, int(CX - 32), y + 48), TIN, radius=3)
        print_rect(d, (int(CX + 32), y - 8, int(CX + 86), y + 8), TIN_DARK, radius=2)
        print_rect(d, (int(CX - 28), y + 68, int(CX - 6), y + 118), TIN_DARK, radius=3)
        print_rect(d, (int(CX + 6), y + 68, int(CX + 28), y + 118), TIN_DARK, radius=3)
        tab_row(d, y + 70, int(CX - 30), int(CX + 30))
    elif kind == "monkey":
        clap = int(round(6 * math.sin(clock(frame))))
        print_ellipse(d, (int(CX - 58), y - 8, int(CX + 58), y + 86), TIN)
        print_ellipse(d, (int(CX - 40), y - 78, int(CX + 40), y - 2), TIN)
        d.ellipse((int(CX - 16), y - 52, int(CX - 4), y - 40), fill=INK)
        d.ellipse((int(CX + 6), y - 52, int(CX + 18), y - 40), fill=INK)
        print_ellipse(d, (int(CX - 18), y - 28, int(CX + 18), y - 6), TIN_DARK)
        print_ellipse(d, (int(CX - 92), y + 18 - clap, int(CX - 48), y + 62 - clap), TIN_DARK)
        print_ellipse(d, (int(CX + 48), y + 18 + clap, int(CX + 92), y + 62 + clap), TIN_DARK)
        print_rect(d, (int(CX - 22), y + 84, int(CX + 22), y + 118), TIN_DARK, radius=6)
        tab_row(d, y + 86, int(CX - 40), int(CX + 40))
    elif kind == "tank":
        print_poly(
            d,
            [
                (int(CX - 96), y + 36),
                (int(CX - 72), y - 4),
                (int(CX + 72), y - 4),
                (int(CX + 96), y + 36),
                (int(CX + 88), y + 78),
                (int(CX - 88), y + 78),
            ],
            TIN,
        )
        print_ellipse(d, (int(CX - 36), y - 48, int(CX + 36), y + 18), TIN)
        print_rect(d, (int(CX + 28), y - 22, int(CX + 108), y - 6), TIN_DARK, radius=2)
        for i in range(-3, 4):
            print_ellipse(d, (int(CX + i * 22 - 16), y + 58, int(CX + i * 22 + 16), y + 102), TIN_DARK)
        tab_row(d, y + 78, int(CX - 80), int(CX + 80))
    elif kind == "copter":
        ang = clock(frame)
        print_ellipse(d, (int(CX - 70), y - 8, int(CX + 70), y + 64), TIN)
        print_rect(d, (int(CX + 60), y + 8, int(CX + 108), y + 28), TIN, radius=4)
        print_ellipse(d, (int(CX + 96), y - 4, int(CX + 124), y + 28), TIN_DARK)
        d.line([(int(CX - 70), y + 72), (int(CX - 88), y + 108)], fill=INK, width=4)
        d.line([(int(CX + 70), y + 72), (int(CX + 88), y + 108)], fill=INK, width=4)
        d.line([(int(CX - 96), y + 108), (int(CX + 96), y + 108)], fill=INK, width=5)
        hx, hy = int(CX), y - 18
        d.ellipse((hx - 10, hy - 10, hx + 10, hy + 10), fill=TIN_DARK)
        for k in range(3):
            a = ang + k * (math.pi * 2 / 3)
            d.line(
                [(hx, hy), (int(hx + math.cos(a) * 92), int(hy + math.sin(a) * 10))],
                fill=INK[:3] + (220,),
                width=5,
            )
        tab_row(d, y + 64, int(CX - 50), int(CX + 50))
    else:
        print_ellipse(d, (int(CX - 72), y - 8, int(CX + 72), y + 86), TIN)
        print_ellipse(d, (int(CX - 38), y - 58, int(CX - 2), y - 18), TIN)
        print_ellipse(d, (int(CX + 4), y - 58, int(CX + 40), y - 18), TIN)
        d.ellipse((int(CX - 26), y - 48, int(CX - 14), y - 36), fill=INK)
        d.ellipse((int(CX + 16), y - 48, int(CX + 28), y - 36), fill=INK)
        print_poly(d, [(int(CX - 70), y + 48), (int(CX - 118), y + 96), (int(CX - 40), y + 78)], TIN_DARK)
        print_poly(d, [(int(CX + 70), y + 48), (int(CX + 118), y + 96), (int(CX + 40), y + 78)], TIN_DARK)
        tab_row(d, y + 84, int(CX - 50), int(CX + 50))
        wheel(d, int(CX - 28), y + 112, 16)
        wheel(d, int(CX + 28), y + 112, 16)
    return layer


def paint_enamel(kind: str, frame: int) -> Image.Image:
    color = ENAMEL[kind]
    layer = blank()
    d = ImageDraw.Draw(layer)
    dy = tap(frame)
    y = int(CY + dy)
    dark = tuple(max(0, c - 36) for c in color)
    hi = tuple(min(255, c + 36) for c in color)
    d.rounded_rectangle((int(CX - 50), y - 8, int(CX + 50), y + 62), radius=8, fill=(*color, 210))
    d.rectangle((int(CX - 54), y + 8, int(CX + 54), y + 22), fill=(*dark, 200))
    d.rectangle((int(CX - 54), y + 36, int(CX + 54), y + 46), fill=(*hi, 90))
    d.polygon(
        [(int(CX - 42), y - 2), (int(CX - 12), y - 16), (int(CX - 20), y + 28)],
        fill=(*hi, 55),
    )
    return layer


def paint_decal(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    layer = blank()
    d = ImageDraw.Draw(layer)
    dy = tap(frame)
    x, y = int(CX), int(CY + dy - 6)
    if kind == "star":
        pts = []
        for i in range(10):
            r = 22 if i % 2 == 0 else 10
            a = -math.pi / 2 + i * math.pi / 5
            pts.append((int(x + math.cos(a) * r), int(y + math.sin(a) * r)))
        d.polygon(pts, fill=(236, 214, 86, 255), outline=INK)
    elif kind == "eight":
        d.rounded_rectangle((x - 18, y - 24, x + 18, y + 24), radius=6, fill=(236, 232, 220, 255), outline=INK, width=3)
        d.ellipse((x - 10, y - 16, x + 10, y - 2), outline=INK, width=3)
        d.ellipse((x - 10, y + 2, x + 10, y + 16), outline=INK, width=3)
    elif kind == "circus":
        d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=(196, 48, 48, 255), outline=INK, width=3)
        d.polygon([(x, y - 14), (x - 12, y + 10), (x + 12, y + 10)], fill=(236, 214, 86, 255))
    else:
        d.polygon(
            [(x, y - 20), (x + 8, y - 2), (x + 22, y - 2), (x + 10, y + 8), (x + 14, y + 22), (x, y + 12), (x - 14, y + 22), (x - 10, y + 8), (x - 22, y - 2), (x - 8, y - 2)],
            fill=(236, 214, 86, 255),
            outline=INK,
        )
    return layer


def paint_key(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    metal = {"brass": (196, 148, 48), "nickel": (168, 172, 176), "painted": (176, 42, 42)}[kind]
    layer = blank()
    d = ImageDraw.Draw(layer)
    ox, oy = AXLE[0], AXLE[1] + tap(frame)
    ang = clock(frame)
    stem = [rot(ox, oy, ang, ox, oy), rot(ox + 42, oy, ang, ox, oy)]
    d.line(stem, fill=(*metal, 255), width=8)
    d.line(stem, fill=INK[:3] + (120,), width=2)
    bow = rot(ox + 58, oy, ang, ox, oy)
    bx, by = bow
    d.ellipse((bx - 16, by - 16, bx + 16, by + 16), outline=(*metal, 255), width=7)
    d.ellipse((bx - 16, by - 16, bx + 16, by + 16), outline=INK, width=2)
    d.ellipse((int(ox - 8), int(oy - 8), int(ox + 8), int(oy + 8)), fill=TIN_DARK, outline=INK, width=2)
    return layer


def paint_spark(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    layer = blank()
    d = ImageDraw.Draw(layer)
    ox, oy = AXLE[0], AXLE[1] + tap(frame)
    ang = clock(frame)
    if kind == "flint":
        for i in range(5):
            a = ang + i * 1.1
            r = 18 + (i % 3) * 8
            d.line(
                [(int(ox), int(oy)), (int(ox + math.cos(a) * r), int(oy + math.sin(a) * r * 0.7))],
                fill=(236, 196, 72, 210),
                width=2,
            )
            d.ellipse(
                (int(ox + math.cos(a) * r - 2), int(oy + math.sin(a) * r * 0.7 - 2), int(ox + math.cos(a) * r + 2), int(oy + math.sin(a) * r * 0.7 + 2)),
                fill=(255, 236, 140, 230),
            )
    else:
        for i in range(4):
            a = ang * 0.5 + i * 1.4
            px = ox - 10 + math.cos(a) * 12
            py = oy - 18 - i * 10 - 6 * math.sin(clock(frame) + i)
            d.ellipse((int(px - 8), int(py - 6), int(px + 10), int(py + 8)), fill=(236, 236, 232, 90))
    return layer


def paint_wear(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    layer = blank()
    d = ImageDraw.Draw(layer)
    dy = tap(frame)
    y = int(CY + dy)
    if kind == "factory":
        d.polygon(
            [(int(CX - 48), y - 80), (int(CX - 10), y - 100), (int(CX - 22), y - 10)],
            fill=(255, 252, 246, 70),
        )
    elif kind == "scuff":
        rng = np.random.RandomState(77)
        for _ in range(14):
            x = int(CX + rng.randint(-50, 50))
            yy = int(y + rng.randint(-70, 70))
            d.line([(x, yy), (x + rng.randint(8, 22), yy + rng.randint(-4, 4))], fill=(255, 252, 246, 90), width=2)
    else:
        rng = np.random.RandomState(91)
        for _ in range(10):
            x = int(CX + rng.randint(-55, 55))
            yy = int(y + rng.randint(-60, 80))
            r = int(rng.randint(4, 12))
            d.ellipse((x - r, yy - r, x + r, yy + r), fill=(118, 72, 36, 140))
    return layer


STACK = ("bench", "chassis", "enamel", "decal", "key", "spark", "wear")

PAINTERS = {
    "bench": {k: (lambda kind: (lambda frame, k=kind: paint_bench(k, frame)))(k) for k in BENCH},
    "chassis": {
        k: (lambda kind: (lambda frame, k=kind: paint_chassis(k, frame)))(k)
        for k in ("robot", "duck", "racer", "soldier", "monkey", "tank", "copter", "frog")
    },
    "enamel": {k: (lambda kind: (lambda frame, k=kind: paint_enamel(k, frame)))(k) for k in ENAMEL},
    "decal": {
        k: (lambda kind: (lambda frame, k=kind: paint_decal(k, frame)))(k)
        for k in ("star", "eight", "circus", "lightning", "none")
    },
    "key": {
        k: (lambda kind: (lambda frame, k=kind: paint_key(k, frame)))(k) for k in ("brass", "nickel", "painted", "none")
    },
    "spark": {
        k: (lambda kind: (lambda frame, k=kind: paint_spark(k, frame)))(k) for k in ("flint", "steam", "none")
    },
    "wear": {
        k: (lambda kind: (lambda frame, k=kind: paint_wear(k, frame)))(k) for k in ("factory", "scuff", "rust", "none")
    },
}

TRAIT_SPEC: dict[str, list[tuple[str, str, int]]] = {
    "bench": [
        ("linoleum", "Linoleum Bench", 22),
        ("felt", "Felt Bench", 20),
        ("crate", "Crate Bench", 20),
        ("enamel", "Enamel Bench", 20),
        ("pine", "Pine Bench", 18),
    ],
    "chassis": [
        ("robot", "Robot Chassis", 16),
        ("duck", "Duck Chassis", 14),
        ("racer", "Racer Chassis", 14),
        ("soldier", "Soldier Chassis", 12),
        ("monkey", "Monkey Chassis", 12),
        ("tank", "Tank Chassis", 12),
        ("copter", "Copter Chassis", 10),
        ("frog", "Frog Chassis", 10),
    ],
    "enamel": [
        ("tomato", "Tomato Enamel", 18),
        ("navy", "Navy Enamel", 16),
        ("mustard", "Mustard Enamel", 16),
        ("chrome", "Chrome Enamel", 14),
        ("mint", "Mint Enamel", 14),
        ("cream", "Cream Enamel", 12),
        ("cherry", "Cherry Enamel", 10),
    ],
    "decal": [
        ("none", "Bare Tin", 22),
        ("star", "Star Decal", 20),
        ("eight", "No. 8 Decal", 20),
        ("circus", "Circus Decal", 20),
        ("lightning", "Lightning Decal", 18),
    ],
    "key": [
        ("none", "No Key", 16),
        ("brass", "Brass Key", 28),
        ("nickel", "Nickel Key", 28),
        ("painted", "Painted Key", 28),
    ],
    "spark": [
        ("none", "Quiet Works", 40),
        ("flint", "Flint Spark", 36),
        ("steam", "Steam Puff", 24),
    ],
    "wear": [
        ("none", "Shop Fresh", 28),
        ("factory", "Factory Gloss", 28),
        ("scuff", "Playroom Scuff", 24),
        ("rust", "Rust Bloom", 20),
    ],
}

SIGNATURES = [
    {"bench": "linoleum", "chassis": "robot", "enamel": "tomato", "decal": "star", "key": "brass", "spark": "flint", "wear": "factory"},
    {"bench": "felt", "chassis": "duck", "enamel": "mustard", "decal": "none", "key": "nickel", "spark": "none", "wear": "scuff"},
    {"bench": "crate", "chassis": "racer", "enamel": "navy", "decal": "eight", "key": "painted", "spark": "flint", "wear": "none"},
    {"bench": "enamel", "chassis": "soldier", "enamel": "cream", "decal": "circus", "key": "brass", "spark": "none", "wear": "rust"},
    {"bench": "pine", "chassis": "monkey", "enamel": "cherry", "decal": "star", "key": "nickel", "spark": "steam", "wear": "factory"},
    {"bench": "linoleum", "chassis": "tank", "enamel": "chrome", "decal": "lightning", "key": "brass", "spark": "flint", "wear": "scuff"},
    {"bench": "felt", "chassis": "copter", "enamel": "mint", "decal": "none", "key": "painted", "spark": "steam", "wear": "none"},
    {"bench": "crate", "chassis": "frog", "enamel": "tomato", "decal": "eight", "key": "nickel", "spark": "none", "wear": "factory"},
    {"bench": "enamel", "chassis": "robot", "enamel": "navy", "decal": "lightning", "key": "none", "spark": "flint", "wear": "rust"},
    {"bench": "pine", "chassis": "duck", "enamel": "cream", "decal": "circus", "key": "brass", "spark": "steam", "wear": "scuff"},
    {"bench": "linoleum", "chassis": "racer", "enamel": "cherry", "decal": "star", "key": "nickel", "spark": "none", "wear": "none"},
    {"bench": "felt", "chassis": "soldier", "enamel": "mustard", "decal": "none", "key": "painted", "spark": "flint", "wear": "factory"},
    {"bench": "crate", "chassis": "monkey", "enamel": "chrome", "decal": "eight", "key": "brass", "spark": "none", "wear": "rust"},
    {"bench": "enamel", "chassis": "tank", "enamel": "mint", "decal": "circus", "key": "none", "spark": "steam", "wear": "scuff"},
    {"bench": "pine", "chassis": "copter", "enamel": "tomato", "decal": "lightning", "key": "nickel", "spark": "flint", "wear": "factory"},
    {"bench": "linoleum", "chassis": "frog", "enamel": "navy", "decal": "star", "key": "painted", "spark": "none", "wear": "none"},
]

TRAIT_LABELS = (
    ("bench", "Bench"),
    ("chassis", "Chassis"),
    ("enamel", "Enamel"),
    ("decal", "Decal"),
    ("key", "Key"),
    ("spark", "Spark"),
    ("wear", "Wear"),
)

COLLECTION_DESCRIPTION = (
    "Virello is a 10,000-piece collection of looping wind-up tin-toy PFP GIFs. "
    "Each toy is stacked from seven plates — bench, chassis, enamel, decal, key, spark, and wear — "
    "then flattened onto one 12-frame GIF. Lithographed enamel on stamped metal. The winding key is the loop."
)

COLLECTION_STORY = (
    "Virello.\n\n"
    "A 10,000-piece collection of looping wind-up tin-toy PFP GIFs on Robinhood Chain. "
    "Each toy is stacked from seven plates — bench, chassis, enamel, decal, key, spark, and wear — "
    "then flattened onto one 12-frame GIF. Eight chassis: robot, duck, racer, soldier, monkey, tank, copter, and frog. "
    "The print is lithographed. The key is the loop.\n\n"
    "Stamped metal on a toy-shop bench, not a snow globe. Not neon tubing. No sticker edge. No egg. "
    "Not a shadow puppet. Not a fold. The toy stays seated on one envelope. The wind-up is the key. One shared clock.\n\n"
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
        "name": "Virello",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Eight chassis share one bench; the winding key is the loop.",
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
                "name": f"Toy #{index}",
                "image": f"/virello-preview/{index}.gif",
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
            f'    image: "{sample["image"]}?v=1",\n'
            f"    attributes: [\n      {attrs},\n    ],\n"
            "  }"
        )
    (SRC_DATA / "virello-gallery.ts").write_text(
        "export type VirelloSample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const virelloSamples: VirelloSample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def write_ts_traits() -> None:
    blurbs = {
        "bench": "The toy-shop counter — linoleum, felt, crate, enamel, pine.",
        "chassis": "The stamped body — robot, duck, racer, soldier, monkey, tank, copter, frog.",
        "enamel": "The litho ink — tomato, navy, mustard, chrome, mint, cream, cherry.",
        "decal": "The chest print — star, number 8, circus, lightning.",
        "key": "The wind-up — brass, nickel, painted. The key is the loop.",
        "spark": "What flies off the works — flint, steam.",
        "wear": "How the tin has lived — factory gloss, playroom scuff, rust bloom.",
    }
    none_labels = {
        "decal": "Bare Tin",
        "key": "No Key",
        "spark": "Quiet Works",
        "wear": "Shop Fresh",
    }
    cats = []
    for key, label in TRAIT_LABELS:
        traits = []
        for trait_id, name, rarity in TRAIT_SPEC[key]:
            if trait_id == "none":
                continue
            traits.append(
                "      { "
                f'id: "{trait_id}", name: "{name}", image: "/virello-traits/{key}/{trait_id}.png", rarity: {rarity} '
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
    (SRC_DATA / "virello-traits.ts").write_text(
        "export type VirelloTrait = {\n"
        "  id: string;\n"
        "  name: string;\n"
        "  image?: string;\n"
        "  rarity: number;\n"
        "};\n\n"
        "export type VirelloTraitCategory = {\n"
        f"  id: {ids};\n"
        "  label: string;\n"
        "  blurb: string;\n"
        "  noneLabel?: string;\n"
        "  traits: VirelloTrait[];\n"
        "};\n\n"
        "/** Bump when APNG layers change so the studio does not keep a stale loop. */\n"
        'export const VIRELLO_ART_VERSION = "virello-v1";\n\n'
        "export const VIRELLO_FRAMES = 12;\n"
        "export const VIRELLO_DURATION_MS = 90;\n\n"
        "export function virelloTraitSrc(path?: string) {\n"
        "  if (!path) return \"\";\n"
        "  return `${path}?v=${VIRELLO_ART_VERSION}`;\n"
        "}\n\n"
        "export const virelloTraitCategories: VirelloTraitCategory[] = [\n"
        + ",\n".join(cats)
        + "\n];\n\n"
        'export const noneVirelloTrait: VirelloTrait = { id: "none", name: "None", rarity: 0 };\n\n'
        "export function virelloCategoryById(id: VirelloTraitCategory[\"id\"]) {\n"
        "  const category = virelloTraitCategories.find((item) => item.id === id);\n"
        "  if (!category) throw new Error(`Unknown Virello trait category: ${id}`);\n"
        "  return category;\n"
        "}\n\n"
        "export function findVirelloTrait(categoryId: VirelloTraitCategory[\"id\"], traitId: string) {\n"
        "  if (traitId === \"none\") return noneVirelloTrait;\n"
        "  return virelloCategoryById(categoryId).traits.find((trait) => trait.id === traitId);\n"
        "}\n\n"
        "export const defaultVirelloSelection = {\n"
        '  bench: "linoleum",\n'
        '  chassis: "robot",\n'
        '  enamel: "tomato",\n'
        '  decal: "star",\n'
        '  key: "brass",\n'
        '  spark: "flint",\n'
        '  wear: "factory",\n'
        "} as const;\n\n"
        "export type VirelloSelection = Record<VirelloTraitCategory[\"id\"], string>;\n\n"
        "export function randomVirelloSelection(): VirelloSelection {\n"
        "  const pick = (category: VirelloTraitCategory) => {\n"
        "    const pool: VirelloTrait[] = category.noneLabel\n"
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
        '    bench: pick(virelloCategoryById("bench")),\n'
        '    chassis: pick(virelloCategoryById("chassis")),\n'
        '    enamel: pick(virelloCategoryById("enamel")),\n'
        '    decal: pick(virelloCategoryById("decal")),\n'
        '    key: pick(virelloCategoryById("key")),\n'
        '    spark: pick(virelloCategoryById("spark")),\n'
        '    wear: pick(virelloCategoryById("wear")),\n'
        "  };\n"
        "}\n\n"
        "export function virelloCombinationCount() {\n"
        "  return virelloTraitCategories.reduce((product, category) => {\n"
        "    const extra = category.noneLabel ? 1 : 0;\n"
        "    return product * (category.traits.length + extra);\n"
        "  }, 1);\n"
        "}\n\n"
        "export function virelloSelectionToLayers(selection: VirelloSelection) {\n"
        '  return (["bench", "chassis", "enamel", "decal", "key", "spark", "wear"] as const)\n'
        "    .map((id) => findVirelloTrait(id, selection[id]))\n"
        "    .filter((trait): trait is VirelloTrait => Boolean(trait?.image))\n"
        "    .map((trait) => virelloTraitSrc(trait.image));\n"
        "}\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array(
        [
            [0.92, 0.86, 0.74],
            [0.78, 0.28, 0.22],
            [0.18, 0.28, 0.42],
            [0.90, 0.72, 0.28],
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
    (META_DIR / "virello-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "virello.json").write_text(
        json.dumps(
            {
                "name": "Virello",
                "symbol": "VIRL",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-virello.gif",
                "featured_image": "/brand/featured-virello.jpg",
                "banner_image": "/brand/banner-virello.png",
                "opensea_banner_image": "/brand/banner-virello-opensea.jpg",
                "external_link": "/virello",
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
        (12, 12, SIZE - 13, SIZE - 13), radius=40, outline=(196, 58, 42, 255), width=4
    )
    logo = Image.alpha_composite(logo, rim)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-virello.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-virello-loop.png",
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

    save_image(lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-virello.png", quality=94)
    save_image(lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-virello-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=28)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=28)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-virello.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(
        gif_frames,
        BRAND_DIR / "collection-virello.gif",
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
        print("Writing Virello brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Virello tin toys…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
