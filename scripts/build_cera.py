#!/usr/bin/env python3
"""Paint Cera — paraffin lava lamps.

Every trait is a 12-frame APNG on a shared 512 canvas and 180ms clock.
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
from paint_kit import FRAMES, SIZE, place_portrait, save_apng, save_image  # noqa: E402

DURATION_MS = 180

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

NIGHT = (10, 8, 16, 255)
CHROME = (148, 158, 176)
GOLD = (255, 196, 48)
MAGENTA = (255, 48, 176)
INK = 8
RING = 6

SILL = {
    "wood": ((22, 12, 16), (14, 8, 10)),
    "formica": ((18, 16, 24), (28, 18, 36)),
    "velvet": ((14, 8, 18), (28, 10, 32)),
    "tile": ((20, 16, 24), (12, 10, 16)),
    "night": ((8, 8, 14), (18, 12, 36)),
}

SILL_BOUNCE = {
    "wood": (255, 40, 140, 58),
    "formica": (40, 255, 230, 52),
    "velvet": (255, 48, 200, 62),
    "tile": (80, 255, 90, 48),
    "night": (160, 70, 255, 56),
}

SOCKET = {
    "rocket": (72, 78, 92),
    "saucer": (132, 92, 28),
    "cone": (32, 72, 44),
    "cube": (96, 24, 40),
    "mushroom": (72, 32, 102),
    "chrome": (78, 88, 102),
    "walnut": (36, 22, 16),
    "ceramic": (42, 38, 52),
}

SOCKET_ACCENT = {
    "rocket": (60, 255, 255),
    "saucer": (255, 210, 40),
    "cone": (80, 255, 90),
    "cube": (255, 40, 90),
    "mushroom": (220, 80, 255),
    "chrome": (180, 230, 255),
    "walnut": (255, 120, 40),
    "ceramic": (255, 70, 200),
}

SERUM = {
    "clear": (170, 230, 255),
    "cyan": (20, 245, 255),
    "amber": (255, 140, 20),
    "violet": (168, 48, 255),
    "green": (40, 255, 90),
}

MELT = {
    "crimson": (255, 36, 88),
    "gold": (255, 230, 40),
    "white": (240, 255, 255),
    "magenta": (255, 40, 210),
    "black": (16, 8, 20),
}

COIL = {
    "dim": (96, 40, 18),
    "orange": (255, 96, 24),
    "whitehot": (255, 252, 220),
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


def chaikin(pts: list[tuple[float, float]], rounds: int = 2) -> list[tuple[int, int]]:
    """Corner-cut a closed polygon so flasks read as blown glass, not facets."""
    pts_f = [(float(x), float(y)) for x, y in pts]
    for _ in range(rounds):
        nxt: list[tuple[float, float]] = []
        n = len(pts_f)
        for i in range(n):
            x0, y0 = pts_f[i]
            x1, y1 = pts_f[(i + 1) % n]
            nxt.append((0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1))
            nxt.append((0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1))
        pts_f = nxt
    return [(int(round(x)), int(round(y))) for x, y in pts_f]


def shade_volume(layer: Image.Image, strength: float = 22.0) -> Image.Image:
    """Two-tone cylinder shade. A smooth ramp posters to a hard split in the GIF."""
    arr = np.array(layer, dtype=np.float32)
    xx = np.linspace(-1.0, 1.0, SIZE, dtype=np.float32)
    ramp = np.where(xx[None, :] > 0.08, strength, np.where(xx[None, :] < -0.12, -strength * 0.45, 0.0))
    vis = arr[..., 3] > 0
    for i in range(3):
        arr[..., i] = np.where(vis, np.clip(arr[..., i] - ramp, 0, 255), arr[..., i])
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def offset_poly(pts: list[tuple[int, int]], px: float) -> list[tuple[int, int]]:
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    out: list[tuple[int, int]] = []
    for x, y in pts:
        dx, dy = x - cx, y - cy
        length = math.hypot(dx, dy) or 1.0
        out.append((int(x + px * dx / length), int(y + px * dy / length)))
    return out


def wax_pts(cx: float, cy: float, rx: float, ry: float, pinch: float, wobble: float, phase: float) -> list[tuple[int, int]]:
    """Irregular paraffin mass. pinch > 0 fat bottom (rising), < 0 fat top (mushroom)."""
    pts: list[tuple[int, int]] = []
    n = 18
    for i in range(n):
        a = -math.pi / 2.0 + i * math.tau / n
        x = math.cos(a)
        y = math.sin(a)
        r = 1.0 + pinch * y + wobble * math.sin(a * 3.0 + phase)
        pts.append((int(cx + rx * x * r), int(cy + ry * y)))
    return pts


FLASK_KINDS = ("taper", "cylinder", "teardrop", "bulb")


def flask_poly(kind: str) -> list[tuple[int, int]]:
    cx = int(CX)
    top = int(NECK_Y)
    bot = int(FLOOR_Y)
    if kind == "taper":
        raw = [
            (cx - 22, top),
            (cx + 22, top),
            (cx + 34, top + 32),
            (cx + 64, 200),
            (cx + 82, bot - 12),
            (cx + 70, bot),
            (cx - 70, bot),
            (cx - 82, bot - 12),
            (cx - 64, 200),
            (cx - 34, top + 32),
        ]
    elif kind == "cylinder":
        raw = [
            (cx - 24, top),
            (cx + 24, top),
            (cx + 40, top + 18),
            (cx + 66, top + 40),
            (cx + 66, bot - 10),
            (cx + 56, bot),
            (cx - 56, bot),
            (cx - 66, bot - 10),
            (cx - 66, top + 40),
            (cx - 40, top + 18),
        ]
    elif kind == "teardrop":
        raw = [
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
    else:
        # bulb — spherical body, short neck
        raw = [
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
    return chaikin(raw, 3)


def liquid_union_mask() -> Image.Image:
    """Oil volume that covers every flask; compose clips it to the selected glass."""
    mask = Image.new("L", (SIZE, SIZE), 0)
    d = ImageDraw.Draw(mask)
    for kind in FLASK_KINDS:
        d.polygon(flask_poly(kind), fill=255)
    return mask.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(0.6))


def flask_mask(kind: str | None = None) -> Image.Image:
    if kind is None:
        return liquid_union_mask()
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).polygon(flask_poly(kind), fill=255)
    return mask.filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(0.6))


def flask_liquid_mask(kind: str) -> Image.Image:
    return flask_mask(kind)


def clip_to_mask(layer: Image.Image, mask: Image.Image) -> Image.Image:
    out = layer.copy()
    out.putalpha(ImageChops.darker(layer.split()[-1], mask))
    return out


def clip_to_inner(layer: Image.Image) -> Image.Image:
    out = layer.copy()
    out.putalpha(ImageChops.darker(layer.split()[-1], flask_mask()))
    return out


LIQUID_CATEGORIES = frozenset({"serum", "melt", "coil"})


def paint_sill(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    a, b = SILL[kind]
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    if kind == "wood":
        grain = 10.0 * np.sin(yy / 7.5 + 0.35 * np.sin(xx / 40.0))
        for i in range(3):
            rgb[..., i] = a[i] + grain * (0.35 if i == 0 else 0.12)
        rgb[yy > 400] = np.array(b, dtype=np.float32)
    elif kind == "formica":
        for i in range(3):
            rgb[..., i] = a[i]
        boomer = np.sin((xx / 28.0) + np.cos(yy / 36.0) * 2.2) * np.sin((xx + yy) / 50.0)
        rgb[boomer > 0.55] = np.array(b, dtype=np.float32)
        kidney = ((xx - 390) ** 2 / 70 ** 2 + (yy - 90) ** 2 / 40 ** 2) < 1.0
        rgb[kidney] = np.array((220, 36, 110), dtype=np.float32)
    elif kind == "velvet":
        nap = 8.0 * np.sin(xx / 11.0) * np.sin(yy / 17.0)
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
        rgb[grout] = np.array((6, 6, 10), dtype=np.float32)
    else:
        for i in range(3):
            rgb[..., i] = a[i] + 6.0 * np.sin((xx + yy) / 90.0)
        window = (xx > 360) & (xx < 490) & (yy > 40) & (yy < 210)
        rgb[window] = np.array((40, 18, 72), dtype=np.float32)
        left_pane = window & (xx < 425)
        rgb[left_pane] = np.array((20, 180, 200), dtype=np.float32) * 0.35 + np.array((12, 8, 28), dtype=np.float32) * 0.65
        right_pane = window & (xx >= 425)
        rgb[right_pane] = np.array((220, 40, 160), dtype=np.float32) * 0.32 + np.array((12, 8, 28), dtype=np.float32) * 0.68
        pane = (np.abs(xx - 425) < 2) | (np.abs(yy - 125) < 2)
        rgb[window & pane] = np.array((8, 6, 14), dtype=np.float32)
    rgb += 2.0 * np.sin(yy / 80.0 + t * 0.05)[..., None]
    cx = SIZE / 2.0
    cy = SIZE / 2.0
    vignette = np.clip((np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) - 160.0) / 240.0, 0.0, 1.0)
    rgb *= (1.0 - 0.58 * vignette)[..., None]
    rng = np.random.RandomState(41)
    rgb += rng.randn(SIZE, SIZE, 1).astype(np.float32) * 1.6
    layer = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    bounce = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bounce)
    bd.ellipse((int(CX - 90), 350, int(CX + 100), 455), fill=(6, 4, 10, 110))
    layer.alpha_composite(bounce.filter(ImageFilter.GaussianBlur(12)))
    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((int(CX - 70), 368, int(CX + 78), 442), fill=SILL_BOUNCE[kind])
    layer.alpha_composite(glow.filter(ImageFilter.GaussianBlur(16)))
    return layer


def paint_socket(kind: str, frame: int) -> Image.Image:
    fill = SOCKET[kind]
    layer = blank()
    d = ImageDraw.Draw(layer)
    cx = int(CX)
    top = int(SOCKET_TOP)
    bot = 448
    dark = tuple(max(0, c - 48) for c in fill)
    lite = tuple(min(255, c + 42) for c in fill)
    ink = NIGHT[:3] + (255,)

    if kind == "rocket":
        body = [(cx - 86, bot), (cx - 58, top + 18), (cx - 28, top), (cx + 28, top), (cx + 58, top + 18), (cx + 86, bot)]
        d.polygon(body, fill=fill + (255,), outline=ink, width=INK)
        d.polygon(
            [(cx - 70, bot - 8), (cx - 40, top + 28), (cx - 22, top + 10), (cx - 8, top + 10), (cx - 8, bot - 8)],
            fill=lite + (70,),
        )
        for y in (top + 22, top + 52, top + 86):
            d.arc((cx - 58, y, cx + 58, y + 22), 10, 170, fill=dark + (200,), width=4)
            d.arc((cx - 58, y, cx + 58, y + 22), 200, 330, fill=lite + (200,), width=3)
        d.ellipse((cx - 20, top - 8, cx + 20, top + 16), fill=CHROME + (255,), outline=ink, width=RING)
    elif kind == "saucer":
        d.ellipse((cx - 118, top + 48, cx + 118, bot + 6), fill=dark + (255,), outline=ink, width=INK)
        d.ellipse((cx - 108, top + 32, cx + 108, bot - 10), fill=fill + (255,), outline=ink, width=INK)
        d.ellipse((cx - 72, top + 14, cx + 72, top + 64), fill=lite + (255,), outline=dark + (255,), width=RING)
        d.arc((cx - 72, top + 14, cx + 72, top + 64), 200, 340, fill=(255, 255, 255, 140), width=5)
        d.ellipse((cx - 30, top - 4, cx + 30, top + 26), fill=CHROME + (255,), outline=ink, width=RING)
    elif kind == "cone":
        d.polygon(
            [(cx - 96, bot), (cx - 22, top), (cx + 22, top), (cx + 96, bot)],
            fill=fill + (255,),
            outline=ink,
            width=INK,
        )
        d.polygon([(cx - 50, bot - 12), (cx - 14, top + 18), (cx - 4, top + 18), (cx - 4, bot - 12)], fill=lite + (80,))
        d.ellipse((cx - 40, top + 36, cx + 40, top + 56), outline=dark + (200,), width=4)
        d.ellipse((cx - 20, top - 6, cx + 20, top + 16), fill=dark + (255,), outline=ink, width=RING)
    elif kind == "cube":
        d.rounded_rectangle((cx - 74, top, cx + 74, bot), radius=10, fill=fill + (255,), outline=ink, width=INK)
        d.rectangle((cx - 74, top + 26, cx + 74, top + 38), fill=dark + (255,))
        d.rectangle((cx - 60, top + 8, cx - 48, bot - 16), fill=lite + (90,))
        d.rounded_rectangle((cx - 20, top + 68, cx + 20, top + 112), radius=4, fill=lite + (220,), outline=dark + (255,), width=3)
        d.ellipse((cx - 8, top + 82, cx + 8, top + 98), fill=NIGHT)
    elif kind == "mushroom":
        d.ellipse((cx - 100, top + 24, cx + 100, bot + 10), fill=fill + (255,), outline=ink, width=INK)
        d.ellipse((cx - 70, top + 70, cx + 70, bot + 4), fill=dark + (80,))
        d.ellipse((cx - 42, top - 10, cx + 42, top + 38), fill=lite + (255,), outline=dark + (255,), width=RING)
        d.arc((cx - 78, top + 36, cx + 78, top + 96), 200, 340, fill=lite + (180,), width=6)
    elif kind == "chrome":
        d.rounded_rectangle((cx - 50, top, cx + 50, bot - 10), radius=8, fill=fill + (255,), outline=ink, width=INK)
        d.rectangle((cx - 46, top + 14, cx - 28, bot - 24), fill=(255, 255, 255, 110))
        d.rectangle((cx + 28, top + 20, cx + 44, bot - 28), fill=dark + (90,))
        d.ellipse((cx - 74, bot - 30, cx + 74, bot + 8), fill=dark + (255,), outline=ink, width=RING)
        d.ellipse((cx - 22, top - 6, cx + 22, top + 16), fill=CHROME + (255,), outline=ink, width=RING)
    elif kind == "walnut":
        d.polygon(
            [(cx - 80, bot), (cx - 50, top + 24), (cx - 22, top), (cx + 22, top), (cx + 50, top + 24), (cx + 80, bot)],
            fill=fill + (255,),
            outline=ink,
            width=INK,
        )
        for y in range(top + 18, bot - 10, 18):
            d.arc((cx - 48, y, cx + 48, y + 16), 12, 168, fill=lite + (150,), width=RING)
        d.polygon([(cx - 36, top + 20), (cx - 18, top + 8), (cx - 12, top + 8), (cx - 12, bot - 16)], fill=lite + (50,))
    else:
        d.rounded_rectangle((cx - 66, top + 8, cx + 66, bot), radius=26, fill=fill + (255,), outline=ink, width=INK)
        d.ellipse((cx - 30, top - 4, cx + 30, top + 30), fill=(255, 255, 255, 50))
        d.arc((cx - 44, top + 48, cx + 44, top + 96), 200, 340, fill=(255, 255, 255, 130), width=5)
        d.ellipse((cx + 18, top + 80, cx + 48, bot - 20), fill=dark + (50,))

    d.ellipse((cx - 38, top - 10, cx + 38, top + 14), fill=CHROME + (240,), outline=ink, width=RING)
    accent = SOCKET_ACCENT[kind]
    d.arc((cx - 42, top - 10, cx + 42, top + 20), 200, 340, fill=accent + (200,), width=4)
    return shade_volume(layer)


def paint_flask(kind: str, frame: int) -> Image.Image:
    layer = blank()
    d = ImageDraw.Draw(layer)
    poly = flask_poly(kind)
    cx = int(CX)
    d.polygon(poly, fill=(20, 28, 44, 48))
    d.polygon(offset_poly(poly, 5), outline=(80, 255, 255, 255), width=5)
    d.polygon(offset_poly(poly, -3), outline=(40, 16, 48, 140), width=2)
    spec = blank()
    sd = ImageDraw.Draw(spec)
    sd.polygon(
        [
            (cx - 36, int(NECK_Y + 28)),
            (cx - 28, int(NECK_Y + 28)),
            (cx - 48, 210),
            (cx - 56, int(FLOOR_Y - 28)),
            (cx - 62, int(FLOOR_Y - 28)),
            (cx - 52, 210),
        ],
        fill=(180, 255, 255, 170),
    )
    layer.alpha_composite(spec.filter(ImageFilter.GaussianBlur(1.2)))
    d.line(
        [(cx + 48, int(NECK_Y + 36)), (cx + 60, 220), (cx + 66, int(FLOOR_Y - 30))],
        fill=(255, 60, 180, 90),
        width=5,
    )
    d.polygon(poly, outline=NIGHT[:3] + (255,), width=INK + 3)
    d.rounded_rectangle(
        (cx - 26, int(NECK_Y - 8), cx + 26, int(NECK_Y + 14)),
        radius=5,
        fill=CHROME + (255,),
        outline=NIGHT[:3] + (255,),
        width=RING,
    )
    d.ellipse((cx - 22, int(NECK_Y - 12), cx + 22, int(NECK_Y + 2)), fill=tuple(min(255, c + 20) for c in CHROME) + (255,))
    return layer


def paint_serum(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    color = SERUM[kind]
    layer = blank()
    alpha = 168 if kind == "clear" else 210
    fill = Image.new("RGBA", (SIZE, SIZE), color + (alpha,))
    fill.putalpha(ImageChops.darker(fill.split()[-1], flask_mask()))
    layer.alpha_composite(fill)
    d = ImageDraw.Draw(layer)
    cx = int(CX)
    d.ellipse((cx - 20, int(NECK_Y + 8), cx + 20, int(NECK_Y + 24)), fill=tuple(min(255, c + 40) for c in color) + (140,))
    arr = np.array(layer, dtype=np.float32)
    yy = np.linspace(0.0, 1.0, SIZE, dtype=np.float32)[:, None]
    heat = np.clip((yy - 0.48) / 0.28, 0.0, 1.0)
    pulse = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t))
    vis = arr[..., 3] > 0
    lift = np.array([min(255.0, c + 40.0) for c in color], dtype=np.float32)
    for i in range(3):
        arr[..., i] = np.where(
            vis,
            arr[..., i] * (1.0 - 0.28 * heat * pulse) + lift[i] * 0.28 * heat * pulse,
            arr[..., i],
        )
    xx = np.linspace(-1.0, 1.0, SIZE, dtype=np.float32)
    edge = np.clip(np.abs(xx[None, :]) - 0.08, 0.0, 1.0)
    for i in range(3):
        arr[..., i] = np.where(vis, arr[..., i] * (1.0 - 0.12 * edge), arr[..., i])
    rng = np.random.RandomState(73)
    streak = rng.randn(SIZE, SIZE).astype(np.float32) * 1.6
    for i in range(3):
        arr[..., i] = np.where(vis, arr[..., i] + streak, arr[..., i])
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    gy = int(FLOOR_Y - 24)
    rad = int(40 + 10 * pulse)
    g.ellipse((cx - rad, gy - 18, cx + rad, int(FLOOR_Y + 4)), fill=color + (int(90 * pulse),))
    bloom = out.filter(ImageFilter.GaussianBlur(7))
    bloom_arr = np.array(bloom)
    bloom_arr[..., 3] = (bloom_arr[..., 3].astype(np.float32) * 0.40).astype(np.uint8)
    bloom = Image.fromarray(bloom_arr, "RGBA")
    out = Image.alpha_composite(bloom, out)
    out.alpha_composite(glow.filter(ImageFilter.GaussianBlur(11)))
    return clip_to_inner(out)


def pingpong(u: float) -> float:
    """Triangle wave on [0, 1, 0, …] so a loop can bounce without a jump."""
    u = u % 2.0
    if u < 0.0:
        u += 2.0
    return u if u < 1.0 else 2.0 - u


_OIL_HALF: np.ndarray | None = None


def oil_half_width(y: float) -> float:
    """Cached half-width of the oil envelope at y, so wax can ricochet off glass."""
    global _OIL_HALF
    if _OIL_HALF is None:
        mask = np.array(liquid_union_mask())
        half = np.full(SIZE, 18.0, dtype=np.float32)
        for row_i, row in enumerate(mask):
            xs = np.flatnonzero(row > 80)
            if xs.size >= 2:
                half[row_i] = 0.5 * float(xs[-1] - xs[0])
        _OIL_HALF = half
    yi = max(0, min(SIZE - 1, int(round(y))))
    return float(_OIL_HALF[yi])


def blob_pose(frame: int, index: int) -> tuple[float, float, float, float, float, float, float]:
    """Full trip: each glob rises to the neck, falls, and bounces off the glass."""
    t = clock(frame)
    phase = index * (math.tau / 4.0)
    theta = t + phase
    travel = 0.5 + 0.5 * math.sin(theta)
    y0 = FLOOR_Y - 14
    y1 = NECK_Y + 12
    y = y0 + (y1 - y0) * travel
    rising = math.cos(theta)
    pinch = 0.42 * rising - 0.32 * (travel * travel)
    narrow = 1.0 - 0.48 * (travel ** 1.35)
    rx = (34.0, 26.0, 30.0, 18.0)[index] * narrow * (1.0 + 0.05 * math.cos(t + index))
    ry = (24.0, 32.0, 20.0, 16.0)[index] * (1.10 + 0.22 * abs(rising))
    wobble = 0.10 + 0.05 * math.sin(t + index)
    wall = max(8.0, oil_half_width(y) - rx * 0.70)
    signed = pingpong(t / math.pi + (0.12, 0.85, 1.38, 0.42)[index]) * 2.0 - 1.0
    squash = abs(signed) ** 2.0
    rx *= 1.0 - 0.30 * squash
    ry *= 1.0 + 0.16 * squash
    x = CX + signed * wall
    return x, y, rx, ry, pinch, wobble, signed


def paint_melt(kind: str, frame: int) -> Image.Image:
    color = MELT[kind]
    lite_amt = 18 if kind in ("white", "gold") else 36
    dark_amt = 20 if kind == "black" else 40
    lite = tuple(min(255, c + lite_amt) for c in color)
    dark = tuple(max(0, c - dark_amt) for c in color)
    if kind == "black":
        lite = (80, 255, 230)
        dark = (255, 40, 180)
    layer = blank()
    d = ImageDraw.Draw(layer)
    cx = int(CX)
    t = clock(frame)
    for i in range(4):
        x, y, rx, ry, pinch, wobble, signed = blob_pose(frame, i)
        pts = wax_pts(x, y, rx, ry, pinch, wobble, t + i * 1.7)
        d.polygon(pts, fill=color + (242,))
        d.line(pts + [pts[0]], fill=dark + (210,), width=3)
        inward = -1.0 if signed >= 0.0 else 1.0
        hx = x + inward * rx * 0.22
        hy = y - ry * 0.28
        hpts = wax_pts(hx, hy, rx * 0.38, ry * 0.32, pinch * 0.4, wobble * 0.4, t)
        d.polygon(hpts, fill=lite + (130 if kind != "white" else 90,))
    puddle_h = 22 + int(4 * math.sin(t))
    d.ellipse((cx - 46, int(FLOOR_Y - 6 - puddle_h), cx + 46, int(FLOOR_Y + 4)), fill=color + (244,))
    d.ellipse((cx - 58, int(FLOOR_Y - 10), cx - 18, int(FLOOR_Y + 6)), fill=color + (220,))
    d.ellipse((cx + 16, int(FLOOR_Y - 12), cx + 54, int(FLOOR_Y + 5)), fill=color + (220,))
    stalk = 28 + int(8 * math.sin(t + 0.4))
    d.polygon(
        [
            (cx - 12, int(FLOOR_Y - 8)),
            (cx + 8, int(FLOOR_Y - 8)),
            (cx + 4, int(FLOOR_Y - stalk)),
            (cx - 6, int(FLOOR_Y - stalk - 6)),
        ],
        fill=color + (236,),
    )
    d.ellipse((cx - 18, int(FLOOR_Y - 14), cx + 22, int(FLOOR_Y + 2)), fill=lite + (70,))
    bloom = layer.filter(ImageFilter.GaussianBlur(6))
    bloom_arr = np.array(bloom)
    bloom_arr[..., 3] = (bloom_arr[..., 3].astype(np.float32) * 0.50).astype(np.uint8)
    layer = Image.alpha_composite(Image.fromarray(bloom_arr, "RGBA"), layer)
    return clip_to_inner(layer.filter(ImageFilter.GaussianBlur(0.4)))


def paint_coil(kind: str, frame: int) -> Image.Image:
    color = COIL[kind]
    t = clock(frame)
    pulse = 0.72 + 0.22 * math.sin(t)
    layer = blank()
    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    cx = int(CX)
    y = int(FLOOR_Y - 10)
    rad = int(34 + 10 * pulse)
    alpha = {"dim": 100, "orange": 170, "whitehot": 210}[kind]
    g.ellipse((cx - rad, y - 18, cx + rad, y + 16), fill=color + (int(alpha * pulse),))
    layer.alpha_composite(glow.filter(ImageFilter.GaussianBlur(9)))
    d = ImageDraw.Draw(layer)
    d.ellipse((cx - 28, y - 6, cx + 28, y + 10), fill=tuple(max(0, c - 20) for c in color) + (90,))
    d.arc((cx - 24, y - 8, cx + 24, y + 8), 20, 200, fill=color + (220,), width=3)
    d.arc((cx - 16, y - 4, cx + 16, y + 8), 200, 340, fill=(255, 240, 200, 160), width=2)
    return clip_to_inner(layer)


def paint_lid(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    fill = LID[kind]
    lite = tuple(min(255, c + 28) for c in fill)
    layer = blank()
    d = ImageDraw.Draw(layer)
    cx = int(CX)
    top = int(NECK_Y - 32)
    ink = NIGHT[:3] + (255,)
    d.rounded_rectangle((cx - 28, top + 10, cx + 28, int(NECK_Y + 8)), radius=6, fill=fill + (255,), outline=ink, width=INK)
    d.ellipse((cx - 32, top, cx + 32, top + 22), fill=fill + (255,), outline=ink, width=RING)
    d.ellipse((cx - 26, top - 6, cx + 26, top + 12), fill=lite + (255,), outline=ink, width=3)
    d.arc((cx - 20, top - 4, cx + 20, top + 10), 200, 340, fill=(255, 255, 255, 150), width=3)
    if kind == "painted":
        d.ellipse((cx - 8, top, cx + 8, top + 10), fill=(255, 220, 80, 230))
    return shade_volume(layer, 22.0)


STACK = ("sill", "socket", "flask", "serum", "melt", "coil", "lid")

PAINTERS = {
    "sill": {k: (lambda kind: (lambda frame, k=kind: paint_sill(k, frame)))(k) for k in SILL},
    "socket": {k: (lambda kind: (lambda frame, k=kind: paint_socket(k, frame)))(k) for k in SOCKET},
    "flask": {k: (lambda kind: (lambda frame, k=kind: paint_flask(k, frame)))(k) for k in FLASK_KINDS},
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
    liquid_mask = flask_liquid_mask(selection["flask"])
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
        else:
            frames = render_trait_frames(category, trait_id)
        if category in LIQUID_CATEGORIES:
            frames = [clip_to_mask(frame, liquid_mask) for frame in frames]
        layers.append(frames)
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
            save_apng(
                render_trait_frames(category, trait_id),
                trait_path(category, trait_id),
                duration_ms=DURATION_MS,
            )
    write_flask_masks()
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


def write_flask_masks() -> None:
    mask_dir = TRAIT_DIR / "flask-mask"
    mask_dir.mkdir(parents=True, exist_ok=True)
    for kind in FLASK_KINDS:
        mask = flask_liquid_mask(kind)
        save_image(Image.merge("RGBA", (mask, mask, mask, mask)), mask_dir / f"{kind}.png")


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
            f'    image: "{sample["image"]}?v=8",\n'
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
        'export const CERA_ART_VERSION = "cera-v8";\n\n'
        "export const CERA_FRAMES = 12;\n"
        "export const CERA_DURATION_MS = 180;\n\n"
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
        "    .map((id) => {\n"
        "      const trait = findCeraTrait(id, selection[id]);\n"
        "      if (!trait?.image) return null;\n"
        "      return { id, src: ceraTraitSrc(trait.image) };\n"
        "    })\n"
        '    .filter((layer): layer is { id: CeraTraitCategory["id"]; src: string } => Boolean(layer));\n'
        "}\n\n"
        "export function ceraFlaskMaskSrc(flask: string) {\n"
        "  return ceraTraitSrc(`/cera-traits/flask-mask/${flask}.png`);\n"
        "}\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array(
        [
            [0.04, 0.03, 0.07],
            [0.95, 0.12, 0.70],
            [0.04, 0.90, 0.95],
            [0.10, 0.04, 0.16],
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
        duration_ms=DURATION_MS,
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
