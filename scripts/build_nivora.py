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
CY = 210.0
RADIUS = 158.0
COLLAR_Y = CY + RADIUS - 14.0

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
    "clear": (210, 224, 230),
    "gin": (176, 204, 186),
    "pine": (92, 128, 98),
    "ink": (48, 62, 92),
    "rose": (176, 132, 148),
    "amber": (176, 142, 78),
    "cobalt": (58, 86, 138),
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


def paint_plinth(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    dark, light = PLINTH[kind]
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    shelf = yy / SIZE
    grain = 7.0 * np.sin(xx / 4.2 + 0.55 * np.sin(yy / 11.0))
    if kind == "marble":
        grain = 8.0 * np.sin((xx + yy) / 28.0) + 4.0 * np.sin(xx / 11.0 - yy / 19.0)
    elif kind == "plastic":
        grain = 4.0 * np.sin(xx / 28.0 + t * 0.2)
    elif kind == "bakelite":
        grain = 3.0 * np.sin(xx / 9.0)
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    for i in range(3):
        rgb[..., i] = dark[i] + (light[i] - dark[i]) * (0.35 + 0.45 * shelf) + grain * 0.35
    rgb += 6.0 * np.sin(yy / 40.0 + t * 0.15)[..., None]
    floor = arr_to_image(rgb)
    draw = ImageDraw.Draw(floor)

    # Turned base: stacked lathe rings, not a stick pelvis.
    top = int(COLLAR_Y) + 2
    colors = [
        tuple(max(0, min(255, int(c * 0.55))) for c in light),
        tuple(max(0, min(255, int((d + l) / 2))) for d, l in zip(dark, light)),
        tuple(max(0, min(255, int(c * 1.05))) for c in light),
    ]
    rings = (
        (top, 38, 118, colors[0]),
        (top + 28, 52, 132, colors[1]),
        (top + 56, 64, 148, colors[2]),
        (top + 86, 58, 140, colors[1]),
        (top + 112, 48, 124, colors[0]),
    )
    for y0, h, half, fill in rings:
        draw.ellipse((int(CX - half), y0, int(CX + half), y0 + h), fill=(*fill, 255))
        draw.arc((int(CX - half), y0, int(CX + half), y0 + h), 200, 340, fill=(255, 245, 220, 70), width=2)

    # Contact shadow under the globe.
    shade = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(shade).ellipse(
        (int(CX - 92), int(COLLAR_Y - 8), int(CX + 92), int(COLLAR_Y + 28)),
        fill=(12, 8, 6, 90),
    )
    shade = shade.filter(ImageFilter.GaussianBlur(8))
    floor.alpha_composite(shade)
    return floor


def paint_bath(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    tint = np.array(BATH[kind], dtype=np.float32)
    dx, dy, dist = sphere_coords()
    inside = dist <= RADIUS
    nx = dx / (RADIUS + 0.001)
    ny = dy / (RADIUS + 0.001)
    caustic = 18.0 * np.exp(-((nx * 0.6) ** 2 + (ny - 0.35) ** 2) / 0.18)
    meniscus = 22.0 * np.exp(-((dist - RADIUS + 10) ** 2) / 80.0)
    swirl = 10.0 * np.sin(np.arctan2(dy, dx) * 3.0 + t)
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    for i in range(3):
        rgb[..., i] = tint[i] * 0.55 + caustic + meniscus * 0.4 + swirl * 0.25
        rgb[..., i] += (1.0 - ny) * 28.0
    alpha = np.zeros((SIZE, SIZE), dtype=np.uint8)
    alpha[inside] = 210 if kind != "clear" else 150
    # Clear liquor still needs a faint body so the dome reads as full.
    if kind == "clear":
        alpha[inside] = np.clip(90 + meniscus[inside] + caustic[inside] * 0.4, 70, 170).astype(np.uint8)
    rgb[~inside] = 0
    return arr_to_image(rgb, alpha)


def _bob(frame: int) -> float:
    return math.sin(clock(frame)) * 4.0


def paint_vista(kind: str, frame: int) -> Image.Image:
    layer = blank()
    d = ImageDraw.Draw(layer)
    bob = _bob(frame)
    ox = 4.0 * math.sin(clock(frame) * 0.5)
    oy = 10.0 + bob
    ground_y = CY + 78 + bob

    def g(x: float, y: float) -> tuple[int, int]:
        return int(CX + ox + x), int(CY + oy + y)

    # Miniature ground inside the liquor, not a stick floor.
    d.ellipse((int(CX - 98), int(ground_y - 10), int(CX + 98), int(ground_y + 32)), fill=(86, 78, 62, 230))
    d.ellipse((int(CX - 70), int(ground_y - 2), int(CX + 70), int(ground_y + 16)), fill=(102, 92, 72, 90))

    if kind == "cabin":
        x0, y0 = g(-40, 22)
        d.rectangle((x0, y0, x0 + 78, y0 + 54), fill=(118, 72, 48, 255))
        d.polygon([(x0 - 10, y0), (x0 + 39, y0 - 40), (x0 + 88, y0)], fill=(92, 42, 32, 255))
        d.rectangle((x0 + 30, y0 + 18, x0 + 50, y0 + 54), fill=(48, 32, 24, 255))
        glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        ImageDraw.Draw(glow).rectangle((x0 + 10, y0 + 14, x0 + 26, y0 + 30), fill=(255, 196, 96, 210))
        layer.alpha_composite(glow.filter(ImageFilter.GaussianBlur(1)))
        d.rectangle((x0 + 56, y0 + 16, x0 + 70, y0 + 30), fill=(48, 32, 24, 180))
    elif kind == "pine":
        for dx, sc in ((-32, 1.0), (22, 0.78), (2, 1.18)):
            px, y0 = g(dx, 12)
            h = int(92 * sc)
            d.polygon([(px, y0 - h), (px - int(30 * sc), y0 + 4), (px + int(30 * sc), y0 + 4)], fill=(46, 92, 58, 255))
            d.polygon(
                [(px, y0 - h + 24), (px - int(38 * sc), y0 + 40), (px + int(38 * sc), y0 + 40)],
                fill=(38, 78, 50, 255),
            )
            d.rectangle((px - 4, y0 + 36, px + 4, y0 + 52), fill=(72, 48, 32, 255))
    elif kind == "lighthouse":
        px, y0 = g(0, 4)
        d.polygon([(px - 22, y0 + 82), (px - 14, y0), (px + 14, y0), (px + 22, y0 + 82)], fill=(214, 210, 198, 255))
        d.rectangle((px - 16, y0 + 18, px + 16, y0 + 32), fill=(196, 64, 54, 220))
        d.rectangle((px - 16, y0 + 48, px + 16, y0 + 62), fill=(196, 64, 54, 220))
        d.rectangle((px - 16, y0 - 10, px + 16, y0 + 8), fill=(232, 226, 214, 255))
        d.polygon([(px - 20, y0 - 8), (px, y0 - 28), (px + 20, y0 - 8)], fill=(196, 64, 54, 255))
        ang = clock(frame)
        beam = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        bd = ImageDraw.Draw(beam)
        tip = (int(px + math.cos(ang) * 96), int(y0 - 4 + math.sin(ang) * 16))
        bd.polygon(
            [(px, y0 - 4), tip, (int(px + math.cos(ang + 0.38) * 74), int(y0 + math.sin(ang) * 10))],
            fill=(255, 220, 140, 110),
        )
        layer.alpha_composite(beam)
    elif kind == "deer":
        px, y0 = g(-8, 28)
        hide = (126, 90, 54, 255)
        d.ellipse((px - 28, y0, px + 30, y0 + 36), fill=hide)
        d.ellipse((px + 14, y0 - 26, px + 48, y0 + 10), fill=hide)
        d.ellipse((px + 34, y0 - 18, px + 48, y0 - 4), fill=hide)
        antler = (96, 68, 40, 255)
        d.line([(px + 24, y0 - 24), (px + 14, y0 - 58)], fill=antler, width=4)
        d.line([(px + 24, y0 - 40), (px + 4, y0 - 52)], fill=antler, width=3)
        d.line([(px + 36, y0 - 22), (px + 48, y0 - 56)], fill=antler, width=4)
        d.line([(px + 40, y0 - 38), (px + 58, y0 - 50)], fill=antler, width=3)
        d.rectangle((px - 18, y0 + 28, px - 10, y0 + 58), fill=(96, 68, 40, 255))
        d.rectangle((px + 10, y0 + 28, px + 18, y0 + 58), fill=(96, 68, 40, 255))
        d.ellipse((px + 38, y0 - 14, px + 44, y0 - 8), fill=(36, 24, 16, 255))
    elif kind == "chapel":
        px, y0 = g(-6, 18)
        d.rectangle((px - 34, y0, px + 46, y0 + 62), fill=(186, 178, 164, 255))
        d.polygon([(px - 42, y0), (px + 6, y0 - 42), (px + 54, y0)], fill=(92, 48, 42, 255))
        d.rectangle((px + 2, y0 - 68, px + 14, y0 - 20), fill=(186, 178, 164, 255))
        d.polygon([(px - 6, y0 - 66), (px + 8, y0 - 90), (px + 22, y0 - 66)], fill=(92, 48, 42, 255))
        d.rectangle((px - 6, y0 + 28, px + 12, y0 + 62), fill=(64, 42, 36, 255))
        d.rectangle((px + 22, y0 + 16, px + 36, y0 + 32), fill=(255, 196, 96, 200))
    elif kind == "tram":
        u = frame / FRAMES
        px = int(CX - 78 + u * 156)
        y0 = int(CY + 16 + bob)
        d.line((int(CX - 96), int(CY - 14), int(CX + 96), int(CY + 6)), fill=(70, 64, 58, 255), width=4)
        d.rectangle((px - 26, y0 - 4, px + 26, y0 + 28), fill=(168, 52, 48, 255))
        d.rounded_rectangle((px - 18, y0 + 4, px + 18, y0 + 18), radius=3, fill=(210, 200, 170, 255))
        d.line((px, y0 - 4, px, int(CY - 8)), fill=(70, 64, 58, 255), width=3)
        d.ellipse((px - 16, y0 + 24, px - 8, y0 + 32), fill=(36, 28, 24, 255))
        d.ellipse((px + 8, y0 + 24, px + 16, y0 + 32), fill=(36, 28, 24, 255))
    elif kind == "bridge":
        y0 = int(ground_y - 4)
        d.ellipse((int(CX - 100), y0 + 8, int(CX + 100), y0 + 36), fill=(64, 92, 108, 160))
        d.polygon(
            [
                (int(CX - 100), y0 + 4),
                (int(CX - 70), y0 - 48),
                (int(CX - 8), y0 - 8),
                (int(CX + 8), y0 - 8),
                (int(CX + 70), y0 - 48),
                (int(CX + 100), y0 + 4),
            ],
            fill=(78, 84, 92, 255),
        )
        d.rectangle((int(CX - 104), y0 - 10, int(CX + 104), y0 + 4), fill=(58, 62, 70, 255))
        d.rectangle((int(CX - 78), y0 + 4, int(CX - 64), y0 + 28), fill=(58, 62, 70, 255))
        d.rectangle((int(CX + 64), y0 + 4, int(CX + 78), y0 + 28), fill=(58, 62, 70, 255))
        d.rectangle((int(CX - 8), y0 + 4, int(CX + 8), y0 + 22), fill=(58, 62, 70, 255))
    else:
        # moon
        mx, my = g(18, -22)
        d.ellipse((mx - 42, my - 42, mx + 42, my + 42), fill=(232, 224, 196, 255))
        d.ellipse((mx - 12, my - 10, mx + 10, my + 12), fill=(196, 186, 158, 255))
        d.ellipse((mx + 14, my + 10, mx + 28, my + 24), fill=(196, 186, 158, 255))
        px, y0 = g(-52, 36)
        d.polygon([(px, y0 - 48), (px - 20, y0 + 10), (px + 20, y0 + 10)], fill=(46, 78, 54, 255))
        d.polygon([(px, y0 - 28), (px - 26, y0 + 16), (px + 26, y0 + 16)], fill=(36, 64, 44, 255))

    return clip_sphere(layer)


def paint_flurry(kind: str, frame: int) -> Image.Image:
    layer = blank()
    d = ImageDraw.Draw(layer)
    color = FLURRY_COLOR[kind]
    t = clock(frame)
    rng = np.random.RandomState({"snow": 4101, "gold": 4102, "ash": 4103, "confetti": 4104, "mica": 4105, "grit": 4106}[kind])
    n = 72 if kind in {"snow", "mica"} else 52
    xs = rng.rand(n) * 2.0 - 1.0
    ys = rng.rand(n)
    sizes = rng.randint(1, 4, n)
    for i in range(n):
        ang = xs[i] * math.pi
        fall = (ys[i] + frame / FRAMES + 0.07 * math.sin(t + i)) % 1.0
        # Wrap inside the sphere: polar radius grows then resets, azimuth drifts.
        rr = (0.18 + 0.78 * fall) * (RADIUS - 8)
        x = CX + math.cos(ang + 0.4 * t) * rr * 0.92
        y = CY - RADIUS * 0.72 + fall * (RADIUS * 1.55)
        if (x - CX) ** 2 + (y - CY) ** 2 > (RADIUS - 6) ** 2:
            continue
        s = int(sizes[i])
        if kind == "gold":
            d.rectangle((int(x), int(y), int(x) + s + 1, int(y) + 2), fill=(*color, 230))
        elif kind == "confetti":
            hue = [(220, 92, 96), (72, 140, 120), (70, 110, 190), (220, 180, 70)][i % 4]
            d.rectangle((int(x), int(y), int(x) + 3, int(y) + 2), fill=(*hue, 230))
        elif kind == "grit":
            d.polygon([(int(x), int(y)), (int(x) + 3, int(y) + 2), (int(x) - 1, int(y) + 3)], fill=(*color, 210))
        else:
            d.ellipse((int(x), int(y), int(x) + s + 1, int(y) + s + 1), fill=(*color, 230))
    return clip_sphere(layer)


def paint_lens(kind: str, frame: int) -> Image.Image:
    layer = blank()
    d = ImageDraw.Draw(layer)
    # Glass rim.
    d.ellipse(
        (int(CX - RADIUS), int(CY - RADIUS), int(CX + RADIUS), int(CY + RADIUS)),
        outline=(236, 242, 246, 90),
        width=3,
    )
    # Specular crescent — a souvenir highlight, not a neon halo.
    spec = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(spec)
    spec_box = (int(CX - 110), int(CY - 140), int(CX + 20), int(CY - 10))
    sd.arc(spec_box, 200, 310, fill=(255, 252, 248, 150), width=14)
    spec = spec.filter(ImageFilter.GaussianBlur(3))
    layer.alpha_composite(spec)

    if kind == "smoked":
        wash = blank()
        ImageDraw.Draw(wash).ellipse(
            (int(CX - RADIUS), int(CY - RADIUS), int(CX + RADIUS), int(CY + RADIUS)),
            fill=(28, 32, 36, 70),
        )
        layer.alpha_composite(clip_sphere(wash))
    elif kind == "bubble":
        for i, (bx, by, br) in enumerate(((0.35, -0.25, 16), (-0.4, 0.15, 11), (0.1, 0.4, 8))):
            x = CX + bx * RADIUS
            y = CY + by * RADIUS + math.sin(clock(frame) + i) * 2
            d.ellipse((int(x - br), int(y - br), int(x + br), int(y + br)), outline=(240, 248, 255, 160), width=2)
    elif kind == "crack":
        d.line(
            [(int(CX + 18), int(CY - 90)), (int(CX + 40), int(CY - 20)), (int(CX + 22), int(CY + 50))],
            fill=(220, 228, 234, 180),
            width=2,
        )
        d.line([(int(CX + 40), int(CY - 20)), (int(CX + 78), int(CY + 8))], fill=(220, 228, 234, 140), width=1)
    elif kind == "frost":
        frost = blank()
        fd = ImageDraw.Draw(frost)
        fd.ellipse(
            (int(CX - RADIUS), int(CY - RADIUS), int(CX + RADIUS), int(CY + RADIUS)),
            fill=(220, 230, 236, 40),
        )
        for i in range(18):
            ang = i / 18 * math.pi * 2 + clock(frame) * 0.05
            x = CX + math.cos(ang) * (RADIUS - 18)
            y = CY + math.sin(ang) * (RADIUS - 18)
            fd.ellipse((int(x - 6), int(y - 4), int(x + 6), int(y + 4)), fill=(236, 242, 246, 70))
        layer.alpha_composite(clip_sphere(frost))
    elif kind == "tint":
        wash = blank()
        ImageDraw.Draw(wash).ellipse(
            (int(CX - RADIUS), int(CY - RADIUS), int(CX + RADIUS), int(CY + RADIUS)),
            fill=(120, 160, 150, 36),
        )
        layer.alpha_composite(clip_sphere(wash))
    return layer


def paint_collar(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    metal = {
        "brass": (186, 148, 58),
        "pewter": (132, 136, 138),
        "copper": (168, 92, 58),
        "black": (36, 34, 34),
    }[kind]
    layer = blank()
    d = ImageDraw.Draw(layer)
    y = int(COLLAR_Y)
    d.ellipse((int(CX - 108), y - 16, int(CX + 108), y + 28), fill=(*metal, 255))
    hi = tuple(min(255, c + 40) for c in metal)
    d.arc((int(CX - 108), y - 16, int(CX + 108), y + 28), 200, 340, fill=(*hi, 180), width=3)
    d.ellipse((int(CX - 96), y - 8, int(CX + 96), y + 14), outline=(20, 16, 12, 80), width=2)
    return layer


def paint_plaque(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    layer = blank()
    d = ImageDraw.Draw(layer)
    y = int(COLLAR_Y + 58)
    x0, x1 = int(CX - 36), int(CX + 36)
    if kind == "year":
        d.rounded_rectangle((x0, y, x1, y + 18), radius=3, fill=(186, 148, 58, 240))
        d.rectangle((x0 + 8, y + 6, x1 - 8, y + 10), fill=(72, 48, 22, 200))
    elif kind == "crest":
        d.ellipse((int(CX - 16), y - 4, int(CX + 16), y + 22), fill=(186, 148, 58, 240))
        d.polygon(
            [(int(CX), y - 2), (int(CX - 8), y + 10), (int(CX + 8), y + 10)],
            fill=(72, 48, 22, 220),
        )
    elif kind == "ribbon":
        d.polygon(
            [(x0, y + 4), (x1, y + 4), (x1 - 6, y + 16), (int(CX), y + 10), (x0 + 6, y + 16)],
            fill=(148, 48, 48, 240),
        )
    else:
        d.rectangle((x0 + 4, y, x1 - 4, y + 16), fill=(214, 210, 198, 240))
        d.ellipse((int(CX - 6), y + 4, int(CX + 6), y + 14), outline=(72, 48, 22, 200), width=2)
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
            f'    image: "{sample["image"]}?v=1",\n'
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
        'export const NIVORA_ART_VERSION = "nivora-v1";\n\n'
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
