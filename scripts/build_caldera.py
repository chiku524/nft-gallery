#!/usr/bin/env python3
"""Paint Caldera — hotel matchbooks.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
The portrait is offset-printed cardboard on a cafe table. The flame is the loop.
Not tin toys. Not snow globes. Not neon tubing. Not leather puppets.
Not origami. Not engraved busts. Not sticker cutouts. Not oval-egg bodies.
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

TRAIT_DIR = ROOT / "public" / "caldera-traits"
PREVIEW_DIR = ROOT / "public" / "caldera-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

CX = 268.0
CY = 248.0
COVER = (int(CX - 72), int(CY - 138), int(CX + 72), int(CY + 28))
MATCH_TIP = (int(CX - 118), int(CY - 96))

SOOT = (28, 22, 18, 255)
PAPER_INK = (42, 32, 26, 255)

CLOTH = {
    "check": ((214, 198, 176), (168, 52, 44)),
    "linen": ((226, 214, 196), (186, 170, 148)),
    "vinyl": ((176, 36, 40), (112, 22, 26)),
    "bar": ((62, 42, 32), (28, 18, 14)),
    "stone": ((168, 166, 160), (118, 116, 112)),
}

SLEEVE = {
    "kraft": (186, 142, 88),
    "ivory": (236, 226, 208),
    "crimson": (148, 36, 40),
    "navy": (28, 42, 72),
    "black": (32, 30, 28),
    "mint": (168, 196, 176),
}

COMB = {
    "white": ((236, 230, 218), (176, 48, 40)),
    "kraft": ((198, 156, 102), (148, 42, 36)),
    "ebony": ((42, 36, 32), (168, 48, 40)),
    "candy": ((236, 220, 214), (196, 36, 72)),
}

STRIKE = {
    "grit": (92, 78, 64),
    "redphos": (148, 42, 36),
    "black": (28, 24, 22),
}

FLAME = {
    "gold": ((255, 214, 92), (236, 92, 28)),
    "blue": ((168, 214, 255), (48, 92, 196)),
    "tall": ((255, 236, 140), (220, 72, 24)),
    "ember": ((236, 118, 48), (92, 28, 18)),
}


def clock(frame: int) -> float:
    return frame / FRAMES * math.pi * 2.0


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def flicker(frame: int) -> float:
    t = clock(frame)
    return 0.82 + 0.18 * math.sin(t * 3.1) + 0.08 * math.sin(t * 7.4)


def paper_tooth(arr: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.RandomState(seed)
    noise = rng.randn(SIZE, SIZE).astype(np.float32)
    return arr + noise[..., None] * 4.5


def paint_cloth(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    a, b = CLOTH[kind]
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    if kind == "check":
        cell = (((xx // 36).astype(np.int32) + (yy // 36).astype(np.int32)) % 2).astype(np.float32)
        for i in range(3):
            rgb[..., i] = a[i] * (1.0 - cell) + b[i] * cell
    elif kind == "linen":
        weave = 8.0 * np.sin(xx / 3.2) + 6.0 * np.sin(yy / 4.1)
        for i in range(3):
            rgb[..., i] = a[i] + weave * 0.35
    elif kind == "vinyl":
        for i in range(3):
            rgb[..., i] = a[i] + 10.0 * np.sin((xx + yy) / 28.0)
        seam = (np.abs(xx - 256) < 3) | (np.abs(yy - 400) < 2)
        rgb[seam] = np.array(b, dtype=np.float32)
    elif kind == "bar":
        grain = 12.0 * np.sin(xx / 9.0 + 0.4 * np.sin(yy / 18.0))
        for i in range(3):
            rgb[..., i] = a[i] + grain * 0.4
        rgb[yy > 390] = np.array(b, dtype=np.float32)
    else:
        for i in range(3):
            rgb[..., i] = a[i] + 9.0 * np.sin((xx + yy) / 22.0)
        vein = np.abs(np.sin((xx * 0.04) + (yy * 0.07))) < 0.08
        rgb[vein] = np.array(b, dtype=np.float32)
    rgb += 2.0 * np.sin(yy / 70.0 + t * 0.04)[..., None]
    rgb = paper_tooth(rgb, 11)
    layer = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    shade = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(shade).ellipse((int(CX - 110), 340, int(CX + 130), 430), fill=(16, 10, 8, 80))
    layer.alpha_composite(shade.filter(ImageFilter.GaussianBlur(10)))
    return layer


def sleeve_body(d: ImageDraw.ImageDraw, fill: tuple[int, int, int], yoff: int = 0) -> None:
    x0, y0, x1, y1 = COVER
    y0 += yoff
    y1 += yoff
    d.rounded_rectangle((x0 - 8, y0 - 10, x1 + 8, y1 + 86), radius=10, fill=(*fill, 255))
    d.rounded_rectangle((x0 - 8, y0 - 10, x1 + 8, y1 + 86), outline=PAPER_INK, width=3)
    # spine crease
    d.line([(x0 - 8, y1 + 8), (x1 + 8, y1 + 8)], fill=PAPER_INK[:3] + (90,), width=2)
    # staple
    d.rectangle((int(CX - 10), y0 - 6, int(CX + 10), y0 + 4), fill=(120, 118, 112, 255), outline=SOOT, width=1)
    # inner flap
    d.rounded_rectangle((x0 + 6, y1 + 10, x1 - 6, y1 + 78), radius=4, fill=tuple(min(255, c + 18) for c in fill) + (255,))
    d.rounded_rectangle((x0 + 6, y1 + 10, x1 - 6, y1 + 78), outline=PAPER_INK, width=2)


def paint_sleeve(kind: str, frame: int) -> Image.Image:
    fill = SLEEVE[kind]
    layer = blank()
    d = ImageDraw.Draw(layer)
    sleeve_body(d, fill)
    # paper tooth overlay
    arr = np.array(layer, dtype=np.float32)
    rng = np.random.RandomState(19 + sum(fill))
    tooth = rng.randn(SIZE, SIZE).astype(np.float32) * 5.0
    alpha = arr[..., 3]
    for i in range(3):
        arr[..., i] = np.where(alpha > 0, arr[..., i] + tooth, arr[..., i])
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")


def paint_inn(kind: str, frame: int) -> Image.Image:
    layer = blank()
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = COVER
    # print panel
    d.rounded_rectangle((x0 + 8, y0 + 8, x1 - 8, y1 - 8), radius=4, fill=(244, 236, 214, 255))
    d.rounded_rectangle((x0 + 8, y0 + 8, x1 - 8, y1 - 8), outline=PAPER_INK, width=2)
    mx, my = int(CX), int((y0 + y1) / 2 - 8)

    if kind == "cactus":
        d.rectangle((mx - 10, my - 8, mx + 10, my + 48), fill=(46, 102, 62, 255))
        d.rectangle((mx - 38, my + 4, mx - 10, my + 18), fill=(46, 102, 62, 255))
        d.rectangle((mx + 10, my + 12, mx + 34, my + 24), fill=(46, 102, 62, 255))
        d.ellipse((mx - 14, my - 22, mx + 14, my + 2), fill=(46, 102, 62, 255))
        d.ellipse((mx - 28, my - 58, mx + 28, my - 18), fill=(232, 168, 64, 255))
    elif kind == "lodge":
        d.polygon([(mx, my - 36), (mx - 40, my + 8), (mx + 40, my + 8)], fill=(92, 46, 36, 255))
        d.rectangle((mx - 28, my + 8, mx + 28, my + 44), fill=(198, 176, 148, 255))
        d.rectangle((mx - 8, my + 20, mx + 8, my + 44), fill=PAPER_INK)
        d.polygon([(mx - 50, my + 44), (mx - 18, my - 4), (mx + 8, my + 44)], fill=(36, 78, 52, 255))
    elif kind == "diner":
        d.ellipse((mx - 28, my - 4, mx + 28, my + 44), fill=(236, 232, 220, 255), outline=PAPER_INK, width=3)
        d.ellipse((mx - 16, my + 8, mx + 16, my + 32), fill=(148, 92, 48, 255))
        d.rectangle((mx - 6, my - 28, mx + 6, my - 2), fill=PAPER_INK)
        d.ellipse((mx - 10, my - 40, mx + 10, my - 24), fill=(148, 36, 40, 255))
    elif kind == "buoy":
        d.rectangle((mx - 14, my - 28, mx + 14, my + 40), fill=(196, 48, 42, 255))
        d.rectangle((mx - 14, my - 4, mx + 14, my + 14), fill=(236, 232, 220, 255))
        d.polygon([(mx - 18, my - 28), (mx, my - 52), (mx + 18, my - 28)], fill=PAPER_INK)
        d.ellipse((mx - 48, my + 36, mx + 48, my + 52), fill=(48, 92, 128, 180))
    elif kind == "crown":
        d.polygon(
            [(mx - 36, my + 24), (mx - 36, my - 8), (mx - 18, my + 8), (mx, my - 28), (mx + 18, my + 8), (mx + 36, my - 8), (mx + 36, my + 24)],
            fill=(212, 168, 48, 255),
        )
        d.ellipse((mx - 8, my - 40, mx + 8, my - 24), fill=(212, 168, 48, 255))
        d.rectangle((mx - 40, my + 24, mx + 40, my + 36), fill=(148, 36, 40, 255))
    elif kind == "shield":
        d.polygon([(mx, my - 40), (mx + 36, my - 16), (mx + 28, my + 28), (mx, my + 44), (mx - 28, my + 28), (mx - 36, my - 16)], fill=(48, 86, 64, 255))
        d.polygon([(mx, my - 22), (mx + 16, my - 6), (mx, my + 20), (mx - 16, my - 6)], fill=(236, 214, 86, 255))
    elif kind == "palm":
        d.rectangle((mx - 6, my + 4, mx + 6, my + 48), fill=(118, 78, 42, 255))
        for ang in (-0.9, -0.3, 0.3, 0.9):
            d.polygon(
                [
                    (mx, my + 8),
                    (int(mx + math.cos(ang - 0.4) * 44), int(my - 28 + math.sin(ang) * 8)),
                    (int(mx + math.cos(ang + 0.4) * 44), int(my - 18 + math.sin(ang) * 8)),
                ],
                fill=(46, 110, 64, 255),
            )
        d.ellipse((mx - 40, my + 40, mx + 40, my + 54), fill=(212, 176, 92, 200))
    else:
        d.rounded_rectangle((mx - 36, my - 28, mx + 36, my + 36), radius=4, fill=(236, 232, 220, 255), outline=PAPER_INK, width=2)
        d.line([(mx - 24, my - 8), (mx + 24, my - 8)], fill=PAPER_INK, width=2)
        d.line([(mx - 24, my + 6), (mx + 12, my + 6)], fill=PAPER_INK, width=2)
        d.line([(mx - 24, my + 20), (mx + 20, my + 20)], fill=PAPER_INK, width=2)
        d.rectangle((mx - 36, my - 44, mx + 36, my - 28), fill=(148, 36, 40, 255))

    # clip to cover panel
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle((x0 + 8, y0 + 8, x1 - 8, y1 - 8), radius=4, fill=255)
    out = blank()
    out.paste(layer, (0, 0))
    out.putalpha(ImageChops_min(out.split()[-1], mask))
    return out


def ImageChops_min(a: Image.Image, b: Image.Image) -> Image.Image:
    from PIL import ImageChops

    return ImageChops.darker(a, b)


def paint_comb(kind: str, frame: int) -> Image.Image:
    stick, head = COMB[kind]
    layer = blank()
    d = ImageDraw.Draw(layer)
    x0, _y0, x1, y1 = COVER
    # book matches
    n = 9
    span = (x1 - 18) - (x0 + 18)
    for i in range(n):
        x = int(x0 + 22 + i * (span / (n - 1)))
        d.rectangle((x - 4, y1 + 16, x + 4, y1 + 70), fill=(*stick, 255))
        d.ellipse((x - 7, y1 + 8, x + 7, y1 + 22), fill=(*head, 255))
        d.ellipse((x - 7, y1 + 8, x + 7, y1 + 22), outline=SOOT, width=1)
    # drawn match
    tx, ty = MATCH_TIP
    d.rectangle((tx - 4, ty + 18, tx + 4, y1 + 64), fill=(*stick, 255), outline=PAPER_INK)
    d.ellipse((tx - 9, ty + 4, tx + 9, ty + 24), fill=(*head, 255), outline=SOOT, width=1)
    return layer


def paint_strike(kind: str, frame: int) -> Image.Image:
    grit = STRIKE[kind]
    layer = blank()
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = COVER
    d.rounded_rectangle((x0 + 16, y1 + 56, x1 - 16, y1 + 74), radius=3, fill=(*grit, 255))
    rng = np.random.RandomState({"grit": 3, "redphos": 5, "black": 7}[kind])
    for _ in range(40):
        x = int(rng.randint(x0 + 20, x1 - 20))
        y = int(rng.randint(y1 + 58, y1 + 72))
        d.point((x, y), fill=(20, 16, 12, 200))
    return layer


def paint_flame(kind: str, frame: int) -> Image.Image:
    hi, lo = FLAME[kind]
    layer = blank()
    d = ImageDraw.Draw(layer)
    tx, ty = MATCH_TIP
    f = flicker(frame)
    h = (72 if kind == "tall" else 48 if kind != "ember" else 28) * f
    w = (18 if kind != "ember" else 14) * (0.75 + 0.25 * math.sin(clock(frame) * 5))
    # teardrop stack
    d.ellipse((int(tx - w), int(ty - h * 0.15), int(tx + w), int(ty + 16)), fill=(*lo, 230))
    d.ellipse((int(tx - w * 0.7), int(ty - h * 0.55), int(tx + w * 0.7), int(ty + 4)), fill=(*hi, 230))
    d.ellipse((int(tx - w * 0.35), int(ty - h * 0.95), int(tx + w * 0.35), int(ty - h * 0.25)), fill=(255, 252, 230, 220))
    if kind == "blue":
        d.ellipse((int(tx - 6), int(ty - 8), int(tx + 6), int(ty + 10)), fill=(255, 244, 220, 200))
    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse(
        (int(tx - 28), int(ty - h - 8), int(tx + 28), int(ty + 20)),
        fill=(*hi, 40),
    )
    layer.alpha_composite(glow.filter(ImageFilter.GaussianBlur(6)))
    return layer


def paint_mark(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    layer = blank()
    d = ImageDraw.Draw(layer)
    x0, y0, x1, _y1 = COVER
    if kind == "room":
        d.rounded_rectangle((x1 - 42, y0 + 14, x1 - 12, y0 + 36), radius=2, fill=(42, 32, 26, 220))
        d.rectangle((x1 - 36, y0 + 22, x1 - 18, y0 + 26), fill=(236, 226, 208, 230))
    elif kind == "foil":
        d.ellipse((x0 + 14, y0 + 14, x0 + 44, y0 + 44), fill=(196, 164, 72, 230), outline=PAPER_INK, width=2)
        d.ellipse((x0 + 22, y0 + 22, x0 + 36, y0 + 36), outline=(92, 64, 24, 200), width=2)
    else:
        d.polygon(
            [(int(CX), y0 + 16), (int(CX) - 12, y0 + 36), (int(CX) + 12, y0 + 36)],
            fill=(148, 36, 40, 230),
        )
    return layer


STACK = ("cloth", "sleeve", "inn", "comb", "strike", "flame", "mark")

PAINTERS = {
    "cloth": {k: (lambda kind: (lambda frame, k=kind: paint_cloth(k, frame)))(k) for k in CLOTH},
    "sleeve": {k: (lambda kind: (lambda frame, k=kind: paint_sleeve(k, frame)))(k) for k in SLEEVE},
    "inn": {
        k: (lambda kind: (lambda frame, k=kind: paint_inn(k, frame)))(k)
        for k in ("cactus", "lodge", "diner", "buoy", "crown", "shield", "palm", "ticket")
    },
    "comb": {k: (lambda kind: (lambda frame, k=kind: paint_comb(k, frame)))(k) for k in COMB},
    "strike": {k: (lambda kind: (lambda frame, k=kind: paint_strike(k, frame)))(k) for k in STRIKE},
    "flame": {k: (lambda kind: (lambda frame, k=kind: paint_flame(k, frame)))(k) for k in FLAME},
    "mark": {
        k: (lambda kind: (lambda frame, k=kind: paint_mark(k, frame)))(k) for k in ("room", "foil", "crest", "none")
    },
}

TRAIT_SPEC: dict[str, list[tuple[str, str, int]]] = {
    "cloth": [
        ("check", "Check Cloth", 22),
        ("linen", "Linen Cloth", 22),
        ("vinyl", "Vinyl Cloth", 20),
        ("bar", "Bar Cloth", 18),
        ("stone", "Stone Cloth", 18),
    ],
    "sleeve": [
        ("kraft", "Kraft Sleeve", 20),
        ("ivory", "Ivory Sleeve", 18),
        ("crimson", "Crimson Sleeve", 16),
        ("navy", "Navy Sleeve", 16),
        ("black", "Black Sleeve", 16),
        ("mint", "Mint Sleeve", 14),
    ],
    "inn": [
        ("cactus", "Cactus Inn", 16),
        ("lodge", "Lodge Inn", 14),
        ("diner", "Diner Inn", 14),
        ("buoy", "Buoy Inn", 12),
        ("crown", "Crown Inn", 12),
        ("shield", "Shield Inn", 12),
        ("palm", "Palm Inn", 10),
        ("ticket", "Ticket Inn", 10),
    ],
    "comb": [
        ("white", "White Comb", 28),
        ("kraft", "Kraft Comb", 26),
        ("ebony", "Ebony Comb", 24),
        ("candy", "Candy Comb", 22),
    ],
    "strike": [
        ("grit", "Grit Strike", 36),
        ("redphos", "Red Phosphor", 34),
        ("black", "Black Strike", 30),
    ],
    "flame": [
        ("gold", "Gold Flame", 32),
        ("blue", "Blue Flame", 24),
        ("tall", "Tall Flame", 24),
        ("ember", "Ember Flame", 20),
    ],
    "mark": [
        ("none", "No Mark", 28),
        ("room", "Room Mark", 26),
        ("foil", "Foil Mark", 24),
        ("crest", "Crest Mark", 22),
    ],
}

SIGNATURES = [
    {"cloth": "check", "sleeve": "kraft", "inn": "cactus", "comb": "white", "strike": "grit", "flame": "gold", "mark": "room"},
    {"cloth": "linen", "sleeve": "ivory", "inn": "lodge", "comb": "kraft", "strike": "redphos", "flame": "ember", "mark": "none"},
    {"cloth": "vinyl", "sleeve": "crimson", "inn": "diner", "comb": "candy", "strike": "black", "flame": "tall", "mark": "foil"},
    {"cloth": "bar", "sleeve": "navy", "inn": "buoy", "comb": "ebony", "strike": "grit", "flame": "blue", "mark": "crest"},
    {"cloth": "stone", "sleeve": "mint", "inn": "crown", "comb": "white", "strike": "redphos", "flame": "gold", "mark": "none"},
    {"cloth": "check", "sleeve": "black", "inn": "shield", "comb": "kraft", "strike": "black", "flame": "tall", "mark": "room"},
    {"cloth": "linen", "sleeve": "kraft", "inn": "palm", "comb": "candy", "strike": "grit", "flame": "ember", "mark": "foil"},
    {"cloth": "vinyl", "sleeve": "ivory", "inn": "ticket", "comb": "white", "strike": "redphos", "flame": "blue", "mark": "none"},
    {"cloth": "bar", "sleeve": "crimson", "inn": "cactus", "comb": "ebony", "strike": "grit", "flame": "gold", "mark": "crest"},
    {"cloth": "stone", "sleeve": "navy", "inn": "diner", "comb": "kraft", "strike": "black", "flame": "tall", "mark": "room"},
    {"cloth": "check", "sleeve": "mint", "inn": "lodge", "comb": "white", "strike": "redphos", "flame": "ember", "mark": "foil"},
    {"cloth": "linen", "sleeve": "black", "inn": "buoy", "comb": "candy", "strike": "grit", "flame": "blue", "mark": "none"},
    {"cloth": "vinyl", "sleeve": "kraft", "inn": "crown", "comb": "ebony", "strike": "black", "flame": "gold", "mark": "room"},
    {"cloth": "bar", "sleeve": "ivory", "inn": "shield", "comb": "white", "strike": "redphos", "flame": "tall", "mark": "crest"},
    {"cloth": "stone", "sleeve": "crimson", "inn": "palm", "comb": "kraft", "strike": "grit", "flame": "ember", "mark": "none"},
    {"cloth": "check", "sleeve": "navy", "inn": "ticket", "comb": "candy", "strike": "black", "flame": "blue", "mark": "foil"},
]

TRAIT_LABELS = (
    ("cloth", "Cloth"),
    ("sleeve", "Sleeve"),
    ("inn", "Inn"),
    ("comb", "Comb"),
    ("strike", "Strike"),
    ("flame", "Flame"),
    ("mark", "Mark"),
)

COLLECTION_DESCRIPTION = (
    "Caldera is a 10,000-piece collection of looping hotel-matchbook PFP GIFs. "
    "Each book is stacked from seven plates — cloth, sleeve, inn, comb, strike, flame, and mark — "
    "then flattened onto one 12-frame GIF. Offset-printed cardboard on a cafe table. The flame is the loop."
)

COLLECTION_STORY = (
    "Caldera.\n\n"
    "A 10,000-piece collection of looping hotel-matchbook PFP GIFs on Robinhood Chain. "
    "Each book is stacked from seven plates — cloth, sleeve, inn, comb, strike, flame, and mark — "
    "then flattened onto one 12-frame GIF. Eight inns: cactus, lodge, diner, buoy, crown, shield, palm, and ticket. "
    "The print is cardboard. The flame is the loop.\n\n"
    "A souvenir matchbook on a cafe cloth, not a tin toy. Not a snow globe. Not neon tubing. No sticker edge. No egg. "
    "Not a shadow puppet. Not a fold. The book stays seated on one envelope. The strike is the flame. One shared clock.\n\n"
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
        "name": "Caldera",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Eight inns share one cover; the flame is the loop.",
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
                "name": f"Match #{index}",
                "image": f"/caldera-preview/{index}.gif",
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
    (SRC_DATA / "caldera-gallery.ts").write_text(
        "export type CalderaSample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const calderaSamples: CalderaSample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def write_ts_traits() -> None:
    blurbs = {
        "cloth": "The cafe table — check, linen, vinyl, bar, stone.",
        "sleeve": "The cardboard stock — kraft, ivory, crimson, navy, black, mint.",
        "inn": "The printed hotel — cactus, lodge, diner, buoy, crown, shield, palm, ticket.",
        "comb": "The matches in the book — white, kraft, ebony, candy.",
        "strike": "The phosphor strip — grit, red phosphor, black.",
        "flame": "What burns — gold, blue, tall, ember. The flame is the loop.",
        "mark": "A room stamp, foil seal, or crest.",
    }
    none_labels = {"mark": "No Mark"}
    cats = []
    for key, label in TRAIT_LABELS:
        traits = []
        for trait_id, name, rarity in TRAIT_SPEC[key]:
            if trait_id == "none":
                continue
            traits.append(
                "      { "
                f'id: "{trait_id}", name: "{name}", image: "/caldera-traits/{key}/{trait_id}.png", rarity: {rarity} '
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
    (SRC_DATA / "caldera-traits.ts").write_text(
        "export type CalderaTrait = {\n"
        "  id: string;\n"
        "  name: string;\n"
        "  image?: string;\n"
        "  rarity: number;\n"
        "};\n\n"
        "export type CalderaTraitCategory = {\n"
        f"  id: {ids};\n"
        "  label: string;\n"
        "  blurb: string;\n"
        "  noneLabel?: string;\n"
        "  traits: CalderaTrait[];\n"
        "};\n\n"
        "/** Bump when APNG layers change so the studio does not keep a stale loop. */\n"
        'export const CALDERA_ART_VERSION = "caldera-v1";\n\n'
        "export const CALDERA_FRAMES = 12;\n"
        "export const CALDERA_DURATION_MS = 90;\n\n"
        "export function calderaTraitSrc(path?: string) {\n"
        "  if (!path) return \"\";\n"
        "  return `${path}?v=${CALDERA_ART_VERSION}`;\n"
        "}\n\n"
        "export const calderaTraitCategories: CalderaTraitCategory[] = [\n"
        + ",\n".join(cats)
        + "\n];\n\n"
        'export const noneCalderaTrait: CalderaTrait = { id: "none", name: "None", rarity: 0 };\n\n'
        "export function calderaCategoryById(id: CalderaTraitCategory[\"id\"]) {\n"
        "  const category = calderaTraitCategories.find((item) => item.id === id);\n"
        "  if (!category) throw new Error(`Unknown Caldera trait category: ${id}`);\n"
        "  return category;\n"
        "}\n\n"
        "export function findCalderaTrait(categoryId: CalderaTraitCategory[\"id\"], traitId: string) {\n"
        "  if (traitId === \"none\") return noneCalderaTrait;\n"
        "  return calderaCategoryById(categoryId).traits.find((trait) => trait.id === traitId);\n"
        "}\n\n"
        "export const defaultCalderaSelection = {\n"
        '  cloth: "check",\n'
        '  sleeve: "kraft",\n'
        '  inn: "cactus",\n'
        '  comb: "white",\n'
        '  strike: "grit",\n'
        '  flame: "gold",\n'
        '  mark: "room",\n'
        "} as const;\n\n"
        "export type CalderaSelection = Record<CalderaTraitCategory[\"id\"], string>;\n\n"
        "export function randomCalderaSelection(): CalderaSelection {\n"
        "  const pick = (category: CalderaTraitCategory) => {\n"
        "    const pool: CalderaTrait[] = category.noneLabel\n"
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
        '    cloth: pick(calderaCategoryById("cloth")),\n'
        '    sleeve: pick(calderaCategoryById("sleeve")),\n'
        '    inn: pick(calderaCategoryById("inn")),\n'
        '    comb: pick(calderaCategoryById("comb")),\n'
        '    strike: pick(calderaCategoryById("strike")),\n'
        '    flame: pick(calderaCategoryById("flame")),\n'
        '    mark: pick(calderaCategoryById("mark")),\n'
        "  };\n"
        "}\n\n"
        "export function calderaCombinationCount() {\n"
        "  return calderaTraitCategories.reduce((product, category) => {\n"
        "    const extra = category.noneLabel ? 1 : 0;\n"
        "    return product * (category.traits.length + extra);\n"
        "  }, 1);\n"
        "}\n\n"
        "export function calderaSelectionToLayers(selection: CalderaSelection) {\n"
        '  return (["cloth", "sleeve", "inn", "comb", "strike", "flame", "mark"] as const)\n'
        "    .map((id) => findCalderaTrait(id, selection[id]))\n"
        "    .filter((trait): trait is CalderaTrait => Boolean(trait?.image))\n"
        "    .map((trait) => calderaTraitSrc(trait.image));\n"
        "}\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array(
        [
            [0.93, 0.90, 0.84],
            [0.82, 0.32, 0.14],
            [0.12, 0.10, 0.08],
            [0.96, 0.72, 0.22],
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
    (META_DIR / "caldera-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "caldera.json").write_text(
        json.dumps(
            {
                "name": "Caldera",
                "symbol": "CALD",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-caldera.gif",
                "featured_image": "/brand/featured-caldera.jpg",
                "banner_image": "/brand/banner-caldera.png",
                "opensea_banner_image": "/brand/banner-caldera-opensea.jpg",
                "external_link": "/caldera",
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
        (12, 12, SIZE - 13, SIZE - 13), radius=40, outline=(232, 93, 4, 255), width=4
    )
    logo = Image.alpha_composite(logo, rim)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-caldera.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-caldera-loop.png",
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

    save_image(lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-caldera.png", quality=94)
    save_image(lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-caldera-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=28)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=28)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-caldera.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(
        gif_frames,
        BRAND_DIR / "collection-caldera.gif",
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
        print("Writing Caldera brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Caldera matchbooks…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
