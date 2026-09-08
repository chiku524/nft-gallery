#!/usr/bin/env python3
"""Paint Nivora — souvenir snow globes.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
The portrait is a dome of liquor on a lathe-turned plinth. Glitter is the loop.
Not neon tubing. Not leather puppets. Not origami facets. Not engraved busts.
Not sticker cutouts. Not oval-egg bodies. Not a dancer.
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

TRAIT_DIR = ROOT / "public" / "nivora-traits"
PREVIEW_DIR = ROOT / "public" / "nivora-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

CX = 256.0
CY = 188.0
RADIUS = 176.0
COLLAR_Y = CY + RADIUS * 0.76
PLINTH_H = 112.0

# Short souvenir cup — almost cylindrical, slight belly, modest foot.
LATHE = (
    (0.00, 120.0),
    (0.16, 114.0),
    (0.34, 110.0),
    (0.54, 116.0),
    (0.74, 112.0),
    (0.88, 122.0),
    (1.00, 128.0),
)

PLINTH = {
    "walnut": ((48, 32, 22), (92, 62, 38)),
    "bakelite": ((36, 16, 18), (78, 28, 32)),
    "brass": ((58, 46, 22), (140, 112, 48)),
    "ceramic": ((48, 46, 44), (168, 162, 154)),
    "plastic": ((28, 42, 52), (86, 118, 138)),
    "ebon": ((18, 16, 16), (42, 36, 34)),
    "cherry": ((62, 28, 24), (128, 58, 46)),
    "marble": ((52, 54, 56), (148, 152, 148)),
}

BATH = {
    "clear": (186, 214, 226),
    "gin": (98, 158, 128),
    "pine": (36, 86, 58),
    "ink": (28, 42, 78),
    "rose": (158, 92, 118),
    "amber": (168, 118, 48),
    "cobalt": (32, 64, 128),
}

FLURRY_COLOR = {
    "snow": (245, 248, 252),
    "gold": (214, 176, 78),
    "ash": (118, 116, 112),
    "confetti": (220, 92, 96),
    "mica": (198, 220, 228),
    "grit": (156, 136, 108),
}


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def clock(frame: int) -> float:
    return 2.0 * math.pi * frame / FRAMES


def arr_to_image(rgb: np.ndarray, alpha: np.ndarray | None = None) -> Image.Image:
    a = np.full((SIZE, SIZE), 255, dtype=np.uint8) if alpha is None else alpha
    stacked = np.dstack([np.clip(rgb, 0, 255).astype(np.uint8), a])
    return Image.fromarray(stacked, "RGBA")


def sphere_coords() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    dx = xx - CX
    dy = yy - CY
    dist = np.sqrt(dx * dx + dy * dy)
    return dx, dy, dist


def clip_sphere(layer: Image.Image, radius: float = RADIUS) -> Image.Image:
    _, _, dist = sphere_coords()
    alpha = np.array(layer.split()[-1], dtype=np.float32)
    edge = np.clip((radius + 1.2 - dist) * 1.6, 0.0, 1.0)
    out = np.array(layer, dtype=np.uint8)
    out[..., 3] = np.clip(alpha * edge, 0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def lathe_radius(y: np.ndarray, y0: float, height: float) -> np.ndarray:
    t = np.clip((y - y0) / height, 0.0, 1.0)
    ts = np.array([k[0] for k in LATHE], dtype=np.float32)
    rs = np.array([k[1] for k in LATHE], dtype=np.float32)
    return np.interp(t, ts, rs).astype(np.float32)


def paint_plinth(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    dark, light = PLINTH[kind]
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    wall = yy / SIZE
    grain = 1.8 * np.sin(xx / 54.0 + 0.35 * np.sin(yy / 42.0))
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    horizon = COLLAR_Y + PLINTH_H * 0.78
    floor_mix = np.clip((yy - horizon) / 70.0, 0.0, 1.0)
    wall_rgb = np.array([30.0, 24.0, 20.0])
    floor_rgb = np.array([14.0, 12.0, 11.0])
    lift = 0.12 + 0.18 * wall
    for i in range(3):
        rgb[..., i] = (wall_rgb[i] * (1.0 + lift) * (1.0 - floor_mix) + floor_rgb[i] * floor_mix) + grain * 0.22
    rgb += 2.0 * np.sin(yy / 80.0 + t * 0.06)[..., None]
    floor = arr_to_image(rgb)

    y0 = COLLAR_Y + 4.0
    r = lathe_radius(yy, y0, PLINTH_H)
    dx = xx - CX
    clearance = r - np.abs(dx)
    in_y = (yy >= y0 - 1.0) & (yy <= y0 + PLINTH_H)
    nx = np.clip(dx / (r + 0.8), -1.0, 1.0)
    lambert = 0.40 + 0.62 * np.clip(0.18 - 0.88 * nx, 0.0, 1.0)
    groove = 2.0 * np.sin((yy - y0) * 0.28)
    turned = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    for i in range(3):
        turned[..., i] = dark[i] + (light[i] - dark[i]) * lambert + groove * 0.28
    if kind == "marble":
        veining = 12.0 * np.sin((xx + yy) / 26.0)
        turned += veining[..., None] * 0.28
    alpha = np.clip(clearance * 1.7, 0.0, 1.0)
    alpha = np.where(in_y, alpha, 0.0)
    wood = arr_to_image(turned, (alpha * 255.0).astype(np.uint8))
    floor.alpha_composite(wood)

    d = ImageDraw.Draw(floor)
    lip_y = int(y0 - 8)
    d.ellipse((int(CX - 118), lip_y, int(CX + 118), lip_y + 26), fill=tuple(max(0, c - 10) for c in dark) + (255,))
    d.ellipse((int(CX - 98), lip_y + 6, int(CX + 98), lip_y + 18), fill=tuple(min(255, c + 36) for c in light) + (95,))

    shade = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(shade).ellipse(
        (int(CX - 128), int(y0 + PLINTH_H - 18), int(CX + 128), int(y0 + PLINTH_H + 22)),
        fill=(8, 6, 4, 110),
    )
    shade = shade.filter(ImageFilter.GaussianBlur(10))
    floor.alpha_composite(shade)
    return floor


def paint_bath(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    tint = np.array(BATH[kind], dtype=np.float32)
    dx, dy, dist = sphere_coords()
    inside = dist <= RADIUS - 1.0
    nx = dx / (RADIUS + 0.001)
    ny = dy / (RADIUS + 0.001)
    rim = np.clip((dist - (RADIUS - 22.0)) / 22.0, 0.0, 1.0)
    depth = np.clip((ny + 0.15) * 0.55, 0.0, 1.0)
    caustic = 28.0 * np.exp(-((nx * 0.55) ** 2 + (ny + 0.55) ** 2) / 0.16)
    swirl = 8.0 * np.sin(np.arctan2(dy, dx) * 2.0 + t * 0.8)
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    for i in range(3):
        rgb[..., i] = tint[i] * (0.42 + 0.28 * (1.0 - depth)) + caustic * 0.85 + swirl * 0.2
        rgb[..., i] *= 1.0 - rim * 0.35
    alpha = np.zeros((SIZE, SIZE), dtype=np.float32)
    body = 118.0 if kind != "clear" else 86.0
    alpha[inside] = body
    alpha[inside] += rim[inside] * 72.0
    alpha[inside] += depth[inside] * 18.0
    if kind == "clear":
        alpha[inside] = np.clip(72.0 + rim[inside] * 80.0 + caustic[inside] * 0.28, 60, 170)
    rgb[~inside] = 0
    alpha[~inside] = 0
    return arr_to_image(rgb, np.clip(alpha, 0, 255).astype(np.uint8))


def _bob(frame: int) -> float:
    return math.sin(clock(frame)) * 3.0


def paint_vista(kind: str, frame: int) -> Image.Image:
    layer = blank()
    d = ImageDraw.Draw(layer)
    bob = _bob(frame)
    # Fake refraction: the souvenir is slightly magnified and offset in the liquor.
    ox = 7.0 + 3.0 * math.sin(clock(frame) * 0.5)
    oy = 22.0 + bob
    sc = 1.22
    ground_y = CY + RADIUS * 0.38 + bob

    def g(x: float, y: float) -> tuple[int, int]:
        return int(CX + ox + x * sc), int(CY + oy + y * sc)

    # Snow mound inside the glycerin, not a muddy cookie plate.
    d.ellipse(
        (int(CX - 118), int(ground_y - 6), int(CX + 118), int(ground_y + 40)),
        fill=(96, 82, 62, 220),
    )
    d.ellipse(
        (int(CX - 108), int(ground_y - 22), int(CX + 108), int(ground_y + 18)),
        fill=(236, 240, 244, 245),
    )
    d.ellipse((int(CX - 56), int(ground_y - 34), int(CX - 8), int(ground_y - 8)), fill=(244, 246, 250, 210))
    d.ellipse((int(CX + 18), int(ground_y - 28), int(CX + 64), int(ground_y - 4)), fill=(244, 246, 250, 180))

    if kind == "cabin":
        x0, y0 = g(-36, 10)
        d.rounded_rectangle((x0, y0, x0 + 96, y0 + 64), radius=4, fill=(128, 74, 44, 255))
        for i in range(5):
            yy = y0 + 4 + i * 12
            fill = (108, 58, 34, 255) if i % 2 else (148, 88, 52, 255)
            d.rectangle((x0 + 3, yy, x0 + 93, yy + 11), fill=fill)
        d.polygon([(x0 - 14, y0 + 2), (x0 + 48, y0 - 48), (x0 + 108, y0 + 2)], fill=(92, 40, 30, 255))
        d.polygon([(x0 - 8, y0 + 6), (x0 + 48, y0 - 38), (x0 + 102, y0 + 6)], fill=(244, 246, 250, 235))
        d.rectangle((x0 + 38, y0 + 24, x0 + 58, y0 + 64), fill=(48, 30, 22, 255))
        glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        ImageDraw.Draw(glow).rectangle((x0 + 10, y0 + 16, x0 + 28, y0 + 34), fill=(255, 198, 92, 230))
        ImageDraw.Draw(glow).rectangle((x0 + 66, y0 + 16, x0 + 84, y0 + 32), fill=(255, 198, 92, 160))
        layer.alpha_composite(glow.filter(ImageFilter.GaussianBlur(1)))
        d.rectangle((x0 + 80, y0 - 32, x0 + 94, y0 + 8), fill=(92, 40, 30, 255))
        d.ellipse((x0 + 78, y0 - 42, x0 + 96, y0 - 24), fill=(64, 58, 52, 200))
        px, py = g(-78, 28)
        d.polygon([(px, py - 42), (px - 16, py + 10), (px + 16, py + 10)], fill=(34, 78, 46, 255))
        d.polygon([(px, py - 22), (px - 22, py + 22), (px + 22, py + 22)], fill=(28, 64, 40, 255))
        d.rectangle((px - 4, py + 18, px + 4, py + 36), fill=(78, 52, 34, 255))
    elif kind == "pine":
        for dx, sc_t, yoff in ((-38, 1.05, 0), (26, 0.82, 10), (2, 1.22, -6)):
            px, y0 = g(dx, 4 + yoff)
            h = int(78 * sc_t)
            w = int(26 * sc_t)
            d.polygon([(px, y0 - h), (px - w, y0 + 6), (px + w, y0 + 6)], fill=(38, 86, 52, 255))
            d.polygon(
                [(px, y0 - int(h * 0.62)), (px - int(w * 1.25), y0 + 28), (px + int(w * 1.25), y0 + 28)],
                fill=(30, 72, 44, 255),
            )
            d.polygon(
                [(px, y0 - int(h * 0.28)), (px - int(w * 1.45), y0 + 52), (px + int(w * 1.45), y0 + 52)],
                fill=(28, 62, 40, 255),
            )
            d.rectangle((px - 5, y0 + 48, px + 5, y0 + 68), fill=(78, 52, 34, 255))
            d.ellipse((px - 8, y0 - h + 6, px + 10, y0 - h + 16), fill=(236, 240, 244, 200))
    elif kind == "lighthouse":
        px, y0 = g(0, -8)
        d.polygon([(px - 26, y0 + 92), (px - 16, y0), (px + 16, y0), (px + 26, y0 + 92)], fill=(226, 220, 206, 255))
        d.rectangle((px - 18, y0 + 16, px + 16, y0 + 32), fill=(188, 52, 46, 255))
        d.rectangle((px - 18, y0 + 48, px + 16, y0 + 64), fill=(188, 52, 46, 255))
        d.rectangle((px - 20, y0 - 14, px + 20, y0 + 8), fill=(236, 230, 216, 255))
        d.polygon([(px - 22, y0 - 12), (px, y0 - 36), (px + 22, y0 - 12)], fill=(188, 52, 46, 255))
        d.ellipse((int(CX - 90), int(ground_y + 4), int(CX + 90), int(ground_y + 28)), fill=(54, 86, 108, 140))
        d.polygon([(px - 40, y0 + 88), (px - 18, y0 + 70), (px + 8, y0 + 92)], fill=(110, 96, 82, 255))
        ang = clock(frame)
        beam = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        bd = ImageDraw.Draw(beam)
        tip = (int(px + math.cos(ang) * 108), int(y0 - 6 + math.sin(ang) * 14))
        bd.polygon(
            [(px, y0 - 6), tip, (int(px + math.cos(ang + 0.42) * 82), int(y0 + math.sin(ang) * 8))],
            fill=(255, 224, 140, 130),
        )
        layer.alpha_composite(beam.filter(ImageFilter.GaussianBlur(1)))
    elif kind == "deer":
        px, y0 = g(-4, 14)
        hide = (142, 98, 58, 255)
        d.ellipse((px - 42, y0 - 8, px + 44, y0 + 48), fill=hide)
        d.ellipse((px - 16, y0 + 6, px + 32, y0 + 50), fill=hide)
        d.ellipse((px + 18, y0 - 36, px + 66, y0 + 16), fill=hide)
        d.polygon([(px + 52, y0 - 10), (px + 78, y0 + 2), (px + 54, y0 + 10)], fill=hide)
        antler = (92, 64, 38, 255)
        d.line([(px + 30, y0 - 28), (px + 18, y0 - 70)], fill=antler, width=6)
        d.line([(px + 28, y0 - 48), (px + 2, y0 - 60)], fill=antler, width=5)
        d.line([(px + 42, y0 - 26), (px + 58, y0 - 68)], fill=antler, width=6)
        d.line([(px + 48, y0 - 44), (px + 72, y0 - 58)], fill=antler, width=5)
        leg = (98, 68, 40, 255)
        for lx, top, bot, w in (
            (px - 32, y0 + 28, y0 + 76, 17),
            (px - 8, y0 + 30, y0 + 78, 16),
            (px + 12, y0 + 26, y0 + 74, 16),
            (px + 30, y0 + 26, y0 + 72, 15),
        ):
            d.rounded_rectangle((lx, top, lx + w, bot), radius=5, fill=leg)
            d.ellipse((lx - 2, bot - 7, lx + w + 5, bot + 6), fill=(72, 48, 28, 255))
        d.ellipse((px + 50, y0 - 18, px + 60, y0 - 8), fill=(32, 22, 14, 255))
        d.ellipse((px - 36, y0 + 10, px - 18, y0 + 28), fill=(122, 84, 48, 255))
    elif kind == "chapel":
        px, y0 = g(-8, 2)
        d.rectangle((px - 40, y0, px + 54, y0 + 70), fill=(198, 188, 172, 255))
        d.polygon([(px - 48, y0), (px + 6, y0 - 46), (px + 62, y0)], fill=(92, 46, 40, 255))
        d.polygon([(px - 40, y0 + 4), (px + 6, y0 - 38), (px + 54, y0 + 4)], fill=(240, 242, 246, 220))
        d.rectangle((px + 2, y0 - 72, px + 18, y0 - 18), fill=(198, 188, 172, 255))
        d.polygon([(px - 6, y0 - 70), (px + 10, y0 - 96), (px + 26, y0 - 70)], fill=(92, 46, 40, 255))
        d.rectangle((px - 8, y0 + 32, px + 14, y0 + 70), fill=(64, 40, 34, 255))
        glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        ImageDraw.Draw(glow).rectangle((px + 26, y0 + 16, px + 44, y0 + 38), fill=(255, 196, 90, 210))
        layer.alpha_composite(glow.filter(ImageFilter.GaussianBlur(1)))
    elif kind == "tram":
        d.polygon(
            [(int(CX - 96), int(ground_y + 4)), (int(CX - 40), int(CY + 8 + bob)), (int(CX + 8), int(ground_y + 8))],
            fill=(72, 88, 78, 220),
        )
        d.polygon(
            [(int(CX + 20), int(ground_y + 6)), (int(CX + 70), int(CY + 18 + bob)), (int(CX + 108), int(ground_y + 8))],
            fill=(62, 78, 70, 200),
        )
        u = frame / FRAMES
        px = int(CX - 86 + u * 168)
        y0 = int(CY + 22 + bob)
        d.line((int(CX - 108), int(CY - 8), int(CX + 108), int(CY + 18)), fill=(62, 56, 50, 255), width=5)
        d.rounded_rectangle((px - 30, y0 - 6, px + 30, y0 + 30), radius=6, fill=(176, 48, 44, 255))
        d.rounded_rectangle((px - 20, y0 + 4, px + 20, y0 + 18), radius=3, fill=(220, 210, 176, 255))
        d.line((px, y0 - 6, px, int(CY + 4)), fill=(62, 56, 50, 255), width=3)
        d.ellipse((px - 18, y0 + 26, px - 8, y0 + 36), fill=(32, 24, 20, 255))
        d.ellipse((px + 8, y0 + 26, px + 18, y0 + 36), fill=(32, 24, 20, 255))
    elif kind == "bridge":
        y0 = int(ground_y - 2)
        d.ellipse((int(CX - 118), y0 + 8, int(CX + 118), y0 + 46), fill=(48, 92, 112, 185))
        d.ellipse((int(CX - 50), y0 + 12, int(CX + 46), y0 + 26), fill=(210, 228, 236, 70))
        stone = (96, 92, 88, 255)
        d.rounded_rectangle((int(CX - 112), y0 - 10, int(CX - 74), y0 + 36), radius=6, fill=stone)
        d.rounded_rectangle((int(CX + 74), y0 - 10, int(CX + 112), y0 + 36), radius=6, fill=stone)
        d.arc((int(CX - 98), y0 - 82, int(CX + 98), y0 + 32), 200, 340, fill=(108, 100, 92, 255), width=24)
        d.rectangle((int(CX - 102), y0 - 18, int(CX + 102), y0 - 2), fill=(72, 76, 82, 255))
        d.line([(int(CX - 92), y0 - 32), (int(CX + 92), y0 - 32)], fill=(58, 62, 70, 220), width=3)
        for i in range(-3, 4):
            x = int(CX + i * 24)
            d.rectangle((x - 2, y0 - 32, x + 2, y0 - 16), fill=(58, 62, 70, 220))
    else:
        mx, my = g(22, -36)
        d.ellipse((mx - 48, my - 48, mx + 48, my + 48), fill=(236, 226, 196, 255))
        d.ellipse((mx - 14, my - 12, mx + 12, my + 14), fill=(198, 186, 154, 255))
        d.ellipse((mx + 16, my + 10, mx + 32, my + 26), fill=(198, 186, 154, 255))
        px, y0 = g(-54, 18)
        d.polygon([(px, y0 - 58), (px - 24, y0 + 16), (px + 24, y0 + 16)], fill=(36, 72, 48, 255))
        d.polygon([(px, y0 - 32), (px - 32, y0 + 28), (px + 32, y0 + 28)], fill=(28, 58, 40, 255))
        d.ellipse((px - 10, y0 - 58, px + 12, y0 - 46), fill=(236, 240, 244, 200))

    return clip_sphere(layer, RADIUS - 4)


def paint_flurry(kind: str, frame: int) -> Image.Image:
    layer = blank()
    d = ImageDraw.Draw(layer)
    color = FLURRY_COLOR[kind]
    t = clock(frame)
    rng = np.random.RandomState({"snow": 4101, "gold": 4102, "ash": 4103, "confetti": 4104, "mica": 4105, "grit": 4106}[kind])
    n = 96 if kind in {"snow", "mica"} else 68
    az = rng.rand(n) * math.pi * 2
    phase = rng.rand(n)
    sizes = rng.randint(5, 10, n)
    inner = RADIUS - 12
    for i in range(n):
        fall = (phase[i] + frame / FRAMES + 0.04 * math.sin(t + i * 0.4)) % 1.0
        phi = (0.16 + 0.78 * fall) * math.pi
        drift = az[i] + 0.28 * t + 0.15 * math.sin(fall * 4.0)
        x = CX + math.sin(phi) * math.cos(drift) * inner
        y = CY - math.cos(phi) * inner * 0.92
        if (x - CX) ** 2 + (y - CY) ** 2 > (RADIUS - 8) ** 2:
            continue
        s = int(sizes[i])
        if kind == "gold":
            d.ellipse((int(x - s * 0.6), int(y), int(x + s * 0.6), int(y) + 3), fill=(*color, 235))
        elif kind == "confetti":
            hue = [(220, 92, 96), (72, 140, 120), (70, 110, 190), (220, 180, 70)][i % 4]
            d.ellipse((int(x - 3), int(y - 2), int(x + 4), int(y) + 3), fill=(*hue, 235))
        elif kind == "grit":
            d.polygon([(int(x), int(y)), (int(x) + 5, int(y) + 2), (int(x) - 2, int(y) + 5)], fill=(*color, 220))
        else:
            d.ellipse((int(x - s * 0.55), int(y - s * 0.55), int(x + s * 0.55), int(y + s * 0.55)), fill=(*color, 235))
    return clip_sphere(layer, RADIUS - 3)


def paint_lens(kind: str, frame: int) -> Image.Image:
    dx, dy, dist = sphere_coords()
    rim = np.clip((dist - (RADIUS - 18.0)) / 18.0, 0.0, 1.0)
    shell = (dist <= RADIUS + 2.5) & (dist >= RADIUS - 16.0)
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    rgb[..., 0] = 232
    rgb[..., 1] = 240
    rgb[..., 2] = 246
    alpha = np.zeros((SIZE, SIZE), dtype=np.float32)
    alpha[shell] = 32 + rim[shell] * 140
    layer = arr_to_image(rgb, np.clip(alpha, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(layer)

    spec = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(spec)
    spec_box = (int(CX - 128), int(CY - 162), int(CX + 22), int(CY - 4))
    sd.arc(spec_box, 198, 318, fill=(255, 252, 248, 200), width=20)
    sd.arc((int(CX - 96), int(CY - 128), int(CX - 8), int(CY - 36)), 210, 300, fill=(255, 252, 248, 90), width=8)
    sd.ellipse((int(CX - 82), int(CY - 122), int(CX - 50), int(CY - 90)), fill=(255, 252, 248, 110))
    spec = spec.filter(ImageFilter.GaussianBlur(2))
    layer.alpha_composite(spec)

    if kind == "smoked":
        wash = blank()
        ImageDraw.Draw(wash).ellipse(
            (int(CX - RADIUS), int(CY - RADIUS), int(CX + RADIUS), int(CY + RADIUS)),
            fill=(22, 26, 30, 78),
        )
        layer.alpha_composite(clip_sphere(wash))
    elif kind == "bubble":
        for i, (bx, by, br) in enumerate(((0.38, -0.28, 18), (-0.42, 0.12, 12), (0.12, 0.38, 9))):
            x = CX + bx * RADIUS
            y = CY + by * RADIUS + math.sin(clock(frame) + i) * 2
            d.ellipse((int(x - br), int(y - br), int(x + br), int(y + br)), outline=(240, 248, 255, 170), width=2)
    elif kind == "crack":
        d.line(
            [(int(CX + 78), int(CY - 108)), (int(CX + 108), int(CY - 22)), (int(CX + 86), int(CY + 64))],
            fill=(220, 228, 234, 200),
            width=2,
        )
        d.line([(int(CX + 108), int(CY - 22)), (int(CX + 132), int(CY + 18))], fill=(220, 228, 234, 150), width=1)
    elif kind == "frost":
        frost = blank()
        fd = ImageDraw.Draw(frost)
        fd.ellipse(
            (int(CX - RADIUS), int(CY - RADIUS), int(CX + RADIUS), int(CY + RADIUS)),
            fill=(220, 230, 236, 36),
        )
        for i in range(22):
            ang = i / 22 * math.pi * 2 + clock(frame) * 0.04
            x = CX + math.cos(ang) * (RADIUS - 16)
            y = CY + math.sin(ang) * (RADIUS - 16)
            fd.ellipse((int(x - 7), int(y - 4), int(x + 7), int(y + 4)), fill=(236, 242, 246, 80))
        layer.alpha_composite(clip_sphere(frost))
    elif kind == "tint":
        wash = blank()
        ImageDraw.Draw(wash).ellipse(
            (int(CX - RADIUS), int(CY - RADIUS), int(CX + RADIUS), int(CY + RADIUS)),
            fill=(110, 150, 140, 40),
        )
        layer.alpha_composite(clip_sphere(wash))
    return layer


def paint_collar(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    metal = {
        "brass": (196, 152, 58),
        "pewter": (138, 140, 142),
        "copper": (176, 92, 54),
        "black": (34, 32, 32),
    }[kind]
    layer = blank()
    d = ImageDraw.Draw(layer)
    y = int(CY + RADIUS * 0.72)
    d.ellipse((int(CX - 122), y - 18, int(CX + 122), y + 34), fill=(*metal, 255))
    hi = tuple(min(255, c + 48) for c in metal)
    lo = tuple(max(0, c - 36) for c in metal)
    d.ellipse((int(CX - 104), y - 4, int(CX + 104), y + 14), fill=(*lo, 255))
    d.arc((int(CX - 122), y - 18, int(CX + 122), y + 34), 200, 340, fill=(*hi, 210), width=5)
    d.arc((int(CX - 118), y - 14, int(CX + 118), y + 28), 20, 160, fill=(*lo, 90), width=3)
    return layer


def paint_plaque(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    layer = blank()
    d = ImageDraw.Draw(layer)
    y = int(COLLAR_Y + 6 + PLINTH_H * 0.46)
    x0, x1 = int(CX - 38), int(CX + 38)
    if kind == "year":
        d.rounded_rectangle((x0, y, x1, y + 20), radius=3, fill=(196, 152, 58, 245))
        d.rectangle((x0 + 10, y + 7, x1 - 10, y + 12), fill=(72, 48, 22, 210))
    elif kind == "crest":
        d.ellipse((int(CX - 18), y - 4, int(CX + 18), y + 24), fill=(196, 152, 58, 245))
        d.polygon(
            [(int(CX), y - 2), (int(CX - 9), y + 12), (int(CX + 9), y + 12)],
            fill=(72, 48, 22, 220),
        )
    elif kind == "ribbon":
        d.polygon(
            [(x0, y + 4), (x1, y + 4), (x1 - 7, y + 18), (int(CX), y + 12), (x0 + 7, y + 18)],
            fill=(156, 44, 44, 245),
        )
    else:
        d.rectangle((x0 + 4, y, x1 - 4, y + 18), fill=(220, 214, 198, 245))
        d.ellipse((int(CX - 7), y + 4, int(CX + 7), y + 16), outline=(72, 48, 22, 210), width=2)
    return layer


PAINTERS = {
    "plinth": {k: (lambda kind: (lambda frame, k=kind: paint_plinth(k, frame)))(k) for k in PLINTH},
    "bath": {k: (lambda kind: (lambda frame, k=kind: paint_bath(k, frame)))(k) for k in BATH},
    "vista": {
        k: (lambda kind: (lambda frame, k=kind: paint_vista(k, frame)))(k)
        for k in ("cabin", "pine", "lighthouse", "deer", "chapel", "tram", "bridge", "moon")
    },
    "flurry": {k: (lambda kind: (lambda frame, k=kind: paint_flurry(k, frame)))(k) for k in FLURRY_COLOR},
    "lens": {k: (lambda kind: (lambda frame, k=kind: paint_lens(k, frame)))(k) for k in ("clear", "smoked", "bubble", "crack", "frost", "tint")},
    "collar": {k: (lambda kind: (lambda frame, k=kind: paint_collar(k, frame)))(k) for k in ("brass", "pewter", "copper", "black")},
    "plaque": {k: (lambda kind: (lambda frame, k=kind: paint_plaque(k, frame)))(k) for k in ("year", "crest", "ribbon", "stamp")},
}

# Vista sits under flurry so flakes fall in front of the souvenir.
STACK = ("plinth", "bath", "vista", "flurry", "lens", "collar", "plaque")

TRAIT_SPEC: dict[str, list[tuple[str, str, int]]] = {
    "plinth": [
        ("walnut", "Walnut Plinth", 18),
        ("bakelite", "Bakelite Plinth", 14),
        ("brass", "Brass Plinth", 12),
        ("ceramic", "Ceramic Plinth", 12),
        ("plastic", "Ice Plastic", 12),
        ("ebon", "Ebon Plinth", 12),
        ("cherry", "Cherry Plinth", 10),
        ("marble", "Marble Plinth", 10),
    ],
    "bath": [
        ("clear", "Clear Bath", 18),
        ("gin", "Gin Bath", 16),
        ("pine", "Pine Bath", 16),
        ("ink", "Ink Bath", 14),
        ("rose", "Rose Bath", 14),
        ("amber", "Amber Bath", 12),
        ("cobalt", "Cobalt Bath", 10),
    ],
    "vista": [
        ("cabin", "Cabin Vista", 18),
        ("pine", "Pine Vista", 16),
        ("lighthouse", "Lighthouse Vista", 14),
        ("deer", "Deer Vista", 12),
        ("chapel", "Chapel Vista", 12),
        ("tram", "Tram Vista", 10),
        ("bridge", "Bridge Vista", 10),
        ("moon", "Moon Vista", 8),
    ],
    "flurry": [
        ("snow", "Snow Flurry", 22),
        ("gold", "Gold Leaf", 16),
        ("ash", "Ash Flurry", 16),
        ("confetti", "Confetti Flurry", 14),
        ("mica", "Mica Flurry", 16),
        ("grit", "Grit Flurry", 16),
    ],
    "lens": [
        ("clear", "Clear Lens", 22),
        ("smoked", "Smoked Lens", 16),
        ("bubble", "Bubble Lens", 16),
        ("crack", "Hairline Crack", 14),
        ("frost", "Frost Lens", 16),
        ("tint", "Tinted Lens", 16),
    ],
    "collar": [
        ("none", "Bare Neck", 22),
        ("brass", "Brass Collar", 22),
        ("pewter", "Pewter Collar", 20),
        ("copper", "Copper Collar", 18),
        ("black", "Black Collar", 16),
    ],
    "plaque": [
        ("none", "No Plaque", 28),
        ("year", "Year Plaque", 18),
        ("crest", "Crest Plaque", 18),
        ("ribbon", "Ribbon Plaque", 18),
        ("stamp", "Stamp Plaque", 18),
    ],
}

SIGNATURES = [
    {"plinth": "walnut", "bath": "gin", "vista": "cabin", "flurry": "snow", "lens": "clear", "collar": "brass", "plaque": "year"},
    {"plinth": "bakelite", "bath": "pine", "vista": "pine", "flurry": "gold", "lens": "smoked", "collar": "pewter", "plaque": "none"},
    {"plinth": "brass", "bath": "ink", "vista": "lighthouse", "flurry": "ash", "lens": "bubble", "collar": "copper", "plaque": "crest"},
    {"plinth": "ceramic", "bath": "rose", "vista": "deer", "flurry": "confetti", "lens": "crack", "collar": "none", "plaque": "ribbon"},
    {"plinth": "plastic", "bath": "amber", "vista": "chapel", "flurry": "mica", "lens": "frost", "collar": "brass", "plaque": "stamp"},
    {"plinth": "ebon", "bath": "cobalt", "vista": "tram", "flurry": "grit", "lens": "tint", "collar": "black", "plaque": "year"},
    {"plinth": "cherry", "bath": "gin", "vista": "bridge", "flurry": "snow", "lens": "clear", "collar": "pewter", "plaque": "none"},
    {"plinth": "marble", "bath": "pine", "vista": "moon", "flurry": "gold", "lens": "smoked", "collar": "copper", "plaque": "crest"},
    {"plinth": "walnut", "bath": "rose", "vista": "pine", "flurry": "mica", "lens": "bubble", "collar": "none", "plaque": "stamp"},
    {"plinth": "bakelite", "bath": "amber", "vista": "cabin", "flurry": "snow", "lens": "frost", "collar": "brass", "plaque": "ribbon"},
    {"plinth": "brass", "bath": "clear", "vista": "deer", "flurry": "gold", "lens": "clear", "collar": "black", "plaque": "none"},
    {"plinth": "ceramic", "bath": "cobalt", "vista": "lighthouse", "flurry": "snow", "lens": "tint", "collar": "pewter", "plaque": "year"},
    {"plinth": "plastic", "bath": "ink", "vista": "chapel", "flurry": "ash", "lens": "crack", "collar": "copper", "plaque": "crest"},
    {"plinth": "ebon", "bath": "gin", "vista": "moon", "flurry": "confetti", "lens": "bubble", "collar": "none", "plaque": "year"},
    {"plinth": "cherry", "bath": "pine", "vista": "tram", "flurry": "grit", "lens": "frost", "collar": "brass", "plaque": "stamp"},
    {"plinth": "marble", "bath": "clear", "vista": "bridge", "flurry": "mica", "lens": "clear", "collar": "black", "plaque": "ribbon"},
]

TRAIT_LABELS = (
    ("plinth", "Plinth"),
    ("bath", "Bath"),
    ("vista", "Vista"),
    ("flurry", "Flurry"),
    ("lens", "Lens"),
    ("collar", "Collar"),
    ("plaque", "Plaque"),
)

COLLECTION_DESCRIPTION = (
    "Nivora is a 10,000-piece collection of looping snow-globe PFP GIFs. "
    "Each souvenir is stacked from seven plates — plinth, bath, vista, flurry, lens, collar, and plaque — "
    "then flattened onto one 12-frame GIF. A dome of liquor on a lathe-turned base. Glitter is the loop."
)

COLLECTION_STORY = (
    "Nivora.\n\n"
    "A 10,000-piece collection of looping snow-globe PFP GIFs on Robinhood Chain. "
    "Each souvenir is stacked from seven plates — plinth, bath, vista, flurry, lens, collar, and plaque — "
    "then flattened onto one 12-frame GIF. Eight vistas: cabin, pine, lighthouse, deer, chapel, tram, bridge, and moon. "
    "Glycerin holds the flake. A collar seats the dome.\n\n"
    "A sphere on a turned plinth, not a dancer. Not neon tubing. No sticker edge. No egg. "
    "Not a shadow puppet. Not a fold. The globe stays seated on one envelope. The weather is the flurry. One shared clock.\n\n"
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
        "name": "Nivora",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Eight vistas share one dome; collar and plaque never edit the vista file.",
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
                "name": f"Globe #{index}",
                "image": f"/nivora-preview/{index}.gif",
                "attributes": [
                    {"trait_type": label, "value": name_of(key, selection[key])} for key, label in TRAIT_LABELS
                ],
            }
        )
    (PREVIEW_DIR / "samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")
    write_ts_gallery(samples)
    write_ts_traits()


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
    (SRC_DATA / "nivora-gallery.ts").write_text(
        "export type NivoraSample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const nivoraSamples: NivoraSample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def write_ts_traits() -> None:
    blurbs = {
        "plinth": "The turned base — walnut, bakelite, brass, ceramic, ice plastic, ebon, cherry, marble.",
        "bath": "The liquor in the dome — clear, gin, pine, ink, rose, amber, cobalt.",
        "vista": "The miniature inside — cabin, pine, lighthouse, deer, chapel, tram, bridge, moon.",
        "flurry": "What falls in the glycerin — snow, gold leaf, ash, confetti, mica, grit.",
        "lens": "The dome glass — clear, smoked, bubble, hairline crack, frost, tint.",
        "collar": "The ring that seats the dome — brass, pewter, copper, black — or bare.",
        "plaque": "A plate on the plinth — year, crest, ribbon, stamp — or none.",
    }
    none_labels = {
        "collar": "Bare Neck",
        "plaque": "No Plaque",
    }
    cats = []
    for key, label in TRAIT_LABELS:
        traits = []
        for trait_id, name, rarity in TRAIT_SPEC[key]:
            if trait_id == "none":
                continue
            traits.append(
                "      { "
                f'id: "{trait_id}", name: "{name}", image: "/nivora-traits/{key}/{trait_id}.png", rarity: {rarity} '
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
    (SRC_DATA / "nivora-traits.ts").write_text(
        "export type NivoraTrait = {\n"
        "  id: string;\n"
        "  name: string;\n"
        "  image?: string;\n"
        "  rarity: number;\n"
        "};\n\n"
        "export type NivoraTraitCategory = {\n"
        f"  id: {ids};\n"
        "  label: string;\n"
        "  blurb: string;\n"
        "  noneLabel?: string;\n"
        "  traits: NivoraTrait[];\n"
        "};\n\n"
        "/** Bump when APNG layers change so the studio does not keep a stale loop. */\n"
        'export const NIVORA_ART_VERSION = "nivora-v3";\n\n'
        "export const NIVORA_FRAMES = 12;\n"
        "export const NIVORA_DURATION_MS = 90;\n\n"
        "export function nivoraTraitSrc(path?: string) {\n"
        "  if (!path) return \"\";\n"
        "  return `${path}?v=${NIVORA_ART_VERSION}`;\n"
        "}\n\n"
        "export const nivoraTraitCategories: NivoraTraitCategory[] = [\n"
        + ",\n".join(cats)
        + "\n];\n\n"
        'export const noneNivoraTrait: NivoraTrait = { id: "none", name: "None", rarity: 0 };\n\n'
        "export function nivoraCategoryById(id: NivoraTraitCategory[\"id\"]) {\n"
        "  const category = nivoraTraitCategories.find((item) => item.id === id);\n"
        "  if (!category) throw new Error(`Unknown Nivora trait category: ${id}`);\n"
        "  return category;\n"
        "}\n\n"
        "export function findNivoraTrait(categoryId: NivoraTraitCategory[\"id\"], traitId: string) {\n"
        "  if (traitId === \"none\") return noneNivoraTrait;\n"
        "  return nivoraCategoryById(categoryId).traits.find((trait) => trait.id === traitId);\n"
        "}\n\n"
        "export const defaultNivoraSelection = {\n"
        '  plinth: "walnut",\n'
        '  bath: "gin",\n'
        '  vista: "cabin",\n'
        '  flurry: "snow",\n'
        '  lens: "clear",\n'
        '  collar: "brass",\n'
        '  plaque: "year",\n'
        "} as const;\n\n"
        "export type NivoraSelection = Record<NivoraTraitCategory[\"id\"], string>;\n\n"
        "export function randomNivoraSelection(): NivoraSelection {\n"
        "  const pick = (category: NivoraTraitCategory) => {\n"
        "    const pool: NivoraTrait[] = category.noneLabel\n"
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
        '    plinth: pick(nivoraCategoryById("plinth")),\n'
        '    bath: pick(nivoraCategoryById("bath")),\n'
        '    vista: pick(nivoraCategoryById("vista")),\n'
        '    flurry: pick(nivoraCategoryById("flurry")),\n'
        '    lens: pick(nivoraCategoryById("lens")),\n'
        '    collar: pick(nivoraCategoryById("collar")),\n'
        '    plaque: pick(nivoraCategoryById("plaque")),\n'
        "  };\n"
        "}\n\n"
        "export function nivoraCombinationCount() {\n"
        "  return nivoraTraitCategories.reduce((product, category) => {\n"
        "    const extra = category.noneLabel ? 1 : 0;\n"
        "    return product * (category.traits.length + extra);\n"
        "  }, 1);\n"
        "}\n\n"
        "export function nivoraSelectionToLayers(selection: NivoraSelection) {\n"
        '  return (["plinth", "bath", "vista", "flurry", "lens", "collar", "plaque"] as const)\n'
        "    .map((id) => findNivoraTrait(id, selection[id]))\n"
        "    .filter((trait): trait is NivoraTrait => Boolean(trait?.image))\n"
        "    .map((trait) => nivoraTraitSrc(trait.image));\n"
        "}\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array(
        [
            [0.08, 0.07, 0.06],
            [0.18, 0.14, 0.10],
            [0.28, 0.32, 0.30],
            [0.78, 0.62, 0.32],
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
    (META_DIR / "nivora-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "nivora.json").write_text(
        json.dumps(
            {
                "name": "Nivora",
                "symbol": "NIVO",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-nivora.gif",
                "featured_image": "/brand/featured-nivora.jpg",
                "banner_image": "/brand/banner-nivora.png",
                "opensea_banner_image": "/brand/banner-nivora-opensea.jpg",
                "external_link": "/nivora",
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
        (12, 12, SIZE - 13, SIZE - 13), radius=40, outline=(201, 162, 90, 255), width=4
    )
    logo = Image.alpha_composite(logo, rim)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-nivora.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-nivora-loop.png",
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

    save_image(lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-nivora.png", quality=94)
    save_image(lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-nivora-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=28)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=28)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-nivora.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(
        gif_frames,
        BRAND_DIR / "collection-nivora.gif",
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
        print("Writing Nivora brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Nivora snow globes…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
