#!/usr/bin/env python3
"""Paint Umbra — dancing shadow-puppet characters.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
The cast stays seated in one envelope. Hinges swing the dance.
Language: leather silhouette, brass brads, cutwork, lamp glow.
Not risograph blots. Not origami facets. Not engraved busts.
Not charcoal, not sticker cutouts, not oval-egg bodies.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gif_bake import save_loop_gif  # noqa: E402
from paint_kit import DURATION_MS, FRAMES, SIZE, place_portrait, save_apng, save_image  # noqa: E402

GIF_COLORS = 128
GIF_DITHER = Image.Dither.NONE

TRAIT_DIR = ROOT / "public" / "umbra-traits"
PREVIEW_DIR = ROOT / "public" / "umbra-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

CLOTHS = ("parchment", "saffron", "dusk", "smoke", "indigo", "rose", "ash", "brass")
EMBERS = ("oil", "coal", "dawn", "hearth", "moon", "forge")
CASTS = ("clown", "knight", "bride", "ogre", "sage", "harper", "bird", "demon")
HINGES = ("none", "brass", "iron", "pearl", "rust")
CUTWORKS = ("none", "dots", "stars", "diamonds", "vine")
LEAFS = ("none", "rim", "tips", "full", "dust")
SOOTS = ("none", "motes", "ribbon", "haze", "spark")

# Lamp-and-hide palette. Not washi dyes, not postage inks, not riso fluorescents.
DYE = {
    "parchment": (243, 230, 200),
    "saffron": (214, 164, 72),
    "dusk": (92, 68, 88),
    "smoke": (168, 160, 148),
    "indigo": (32, 40, 72),
    "rose": (176, 96, 92),
    "ash": (120, 116, 108),
    "brass": (184, 140, 64),
}

HIDE = {
    "clown": (36, 22, 18),
    "knight": (24, 28, 36),
    "bride": (48, 28, 40),
    "ogre": (40, 28, 18),
    "sage": (28, 32, 28),
    "harper": (32, 24, 28),
    "bird": (22, 26, 34),
    "demon": (48, 16, 16),
}

METAL = {
    "brass": (196, 148, 58),
    "iron": (88, 88, 92),
    "pearl": (228, 220, 204),
    "rust": (148, 72, 36),
}


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def clock(frame: int) -> float:
    return frame / FRAMES * math.tau


def seed_for(*parts: object) -> int:
    payload = "|".join(map(str, parts)).encode()
    return int(hashlib.md5(payload).hexdigest()[:8], 16)


def shade(rgb: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(max(0, min(255, int(c * amount))) for c in rgb)


def rot(p: tuple[float, float], origin: tuple[float, float], ang: float) -> tuple[float, float]:
    s, c = math.sin(ang), math.cos(ang)
    x, y = p[0] - origin[0], p[1] - origin[1]
    return (origin[0] + x * c - y * s, origin[1] + x * s + y * c)


def rotate_poly(points: list[tuple[float, float]], origin: tuple[float, float], ang: float) -> list[tuple[float, float]]:
    return [rot(p, origin, ang) for p in points]


def wedge(a: tuple[float, float], b: tuple[float, float], width: float) -> list[tuple[float, float]]:
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / length * width, dx / length * width
    tip = width * 0.45
    return [
        (a[0] + nx, a[1] + ny),
        (a[0] - nx, a[1] - ny),
        (b[0] - nx * tip / width, b[1] - ny * tip / width),
        (b[0] + nx * tip / width, b[1] + ny * tip / width),
    ]


def draw_poly(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], fill: tuple) -> None:
    if len(points) < 3:
        return
    draw.polygon([(int(x), int(y)) for x, y in points], fill=fill)


def screen_mask() -> np.ndarray:
    """A taut cloth rectangle — woven screen, not deckle washi, not stamp teeth."""
    layer = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(layer).rectangle((28, 28, SIZE - 29, SIZE - 29), fill=255)
    return np.asarray(layer, dtype=np.uint8)


def paint_cloth(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    base = np.array(DYE[kind], dtype=np.float32)
    rng = np.random.RandomState(seed_for("cloth", kind))
    yy = np.arange(SIZE, dtype=np.float32)[:, None]
    xx = np.arange(SIZE, dtype=np.float32)[None, :]
    t = clock(frame)
    # Warp and weft — a lamp screen, slightly breathing.
    warp = np.sin(xx * 0.42 + t * 0.2) * 2.4
    weft = np.sin(yy * 0.55 + xx * 0.04) * 2.0
    grain = rng.randn(SIZE, SIZE).astype(np.float32) * 1.8
    rgb = np.clip(base + warp[..., None] + weft[..., None] + grain[..., None], 0, 255).astype(np.uint8)
    alpha = screen_mask()
    return Image.fromarray(np.dstack([rgb, alpha]), "RGBA")


def paint_ember(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    t = clock(frame)
    pulse = 0.82 + 0.18 * math.sin(t)
    colors = {
        "oil": (232, 168, 64),
        "coal": (196, 72, 36),
        "dawn": (255, 196, 140),
        "hearth": (220, 96, 48),
        "moon": (196, 208, 220),
        "forge": (255, 120, 48),
    }
    rgb = colors[kind]
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    cx, cy = 256.0, 390.0
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2 * 0.72)
    glow = np.clip(1.0 - dist / (210 * pulse), 0, 1) ** 1.6
    window = screen_mask().astype(np.float32) / 255.0
    out = np.zeros((SIZE, SIZE, 4), dtype=np.uint8)
    out[..., 0] = rgb[0]
    out[..., 1] = rgb[1]
    out[..., 2] = rgb[2]
    out[..., 3] = np.clip(glow * window * 150, 0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def dance_angles(kind: str, frame: int) -> dict[str, float]:
    """Each cast has its own step. Limbs hinge; the torso stays in the envelope."""
    t = clock(frame)
    s, c = math.sin(t), math.cos(t)
    if kind == "clown":
        return {"larm": 0.9 + s * 0.55, "rarm": -0.7 + c * 0.5, "lleg": 0.35 + s * 0.45, "rleg": -0.15 + c * 0.2, "torso": s * 0.06}
    if kind == "knight":
        return {"larm": 0.4 + c * 0.2, "rarm": -1.35 + s * 0.35, "lleg": 0.2 + s * 0.25, "rleg": -0.25 + c * 0.3, "torso": c * 0.04}
    if kind == "bride":
        return {"larm": 1.1 + s * 0.4, "rarm": -1.1 + s * 0.4, "lleg": 0.15 + c * 0.18, "rleg": -0.15 - c * 0.18, "torso": s * 0.08}
    if kind == "ogre":
        return {"larm": 0.55 + s * 0.25, "rarm": -0.55 - s * 0.25, "lleg": 0.45 + (1 if frame % 6 < 3 else -0.1), "rleg": -0.1, "torso": 0.02}
    if kind == "sage":
        return {"larm": 0.2 + c * 0.15, "rarm": -0.85 + s * 0.4, "lleg": 0.12 + s * 0.12, "rleg": -0.12, "torso": s * 0.03}
    if kind == "harper":
        return {"larm": 0.65 + s * 0.5, "rarm": -0.35 + c * 0.35, "lleg": 0.2 + s * 0.2, "rleg": -0.22 + c * 0.18, "torso": c * 0.05}
    if kind == "bird":
        return {"larm": 1.35 + s * 0.55, "rarm": -1.35 - s * 0.55, "lleg": 0.25 + c * 0.2, "rleg": -0.25 - c * 0.2, "torso": s * 0.07}
    # demon
    return {"larm": 0.85 + s * 0.4, "rarm": -0.85 + c * 0.4, "lleg": 0.3 + s * 0.3, "rleg": -0.35 + c * 0.25, "torso": s * 0.09}


def joints() -> dict[str, tuple[float, float]]:
    return {
        "neck": (256.0, 176.0),
        "lsh": (214.0, 204.0),
        "rsh": (298.0, 204.0),
        "lhip": (236.0, 292.0),
        "rhip": (276.0, 292.0),
    }


def paint_cast(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    canvas = blank()
    draw = ImageDraw.Draw(canvas, "RGBA")
    hide = HIDE[kind] + (255,)
    dark = shade(HIDE[kind], 0.7) + (255,)
    ang = dance_angles(kind, frame)
    j = joints()
    torso_origin = (256.0, 248.0)

    torso = rotate_poly(
        [(216, 196), (296, 196), (308, 292), (256, 318), (204, 292)],
        torso_origin,
        ang["torso"],
    )
    draw_poly(draw, torso, hide)

    # Head — angular, not an egg. Each cast gets its own crown.
    neck = rot(j["neck"], torso_origin, ang["torso"])
    if kind == "clown":
        draw_poly(draw, [(neck[0] - 22, neck[1] - 8), (neck[0] + 22, neck[1] - 8), (neck[0] + 16, neck[1] - 48), (neck[0], neck[1] - 62), (neck[0] - 16, neck[1] - 48)], hide)
        for i, dx in enumerate((-18, 0, 18)):
            draw_poly(draw, [(neck[0] + dx - 8, neck[1] - 58), (neck[0] + dx + 8, neck[1] - 58), (neck[0] + dx, neck[1] - 78)], dark)
    elif kind == "knight":
        draw_poly(draw, [(neck[0] - 20, neck[1] - 6), (neck[0] + 20, neck[1] - 6), (neck[0] + 18, neck[1] - 44), (neck[0] - 18, neck[1] - 44)], hide)
        draw_poly(draw, [(neck[0] - 6, neck[1] - 44), (neck[0] + 6, neck[1] - 44), (neck[0], neck[1] - 78)], dark)
    elif kind == "bride":
        draw_poly(draw, [(neck[0] - 18, neck[1] - 6), (neck[0] + 18, neck[1] - 6), (neck[0] + 14, neck[1] - 42), (neck[0] - 14, neck[1] - 42)], hide)
        veil = [(neck[0] - 36, neck[1] - 20), (neck[0] + 36, neck[1] - 20), (neck[0] + 48, neck[1] + 40), (neck[0] - 48, neck[1] + 40)]
        draw_poly(draw, veil, shade(HIDE[kind], 0.55) + (180,))
    elif kind == "ogre":
        draw_poly(draw, [(neck[0] - 26, neck[1] - 4), (neck[0] + 26, neck[1] - 4), (neck[0] + 22, neck[1] - 40), (neck[0] - 22, neck[1] - 40)], hide)
        draw_poly(draw, [(neck[0] - 22, neck[1] - 40), (neck[0] - 34, neck[1] - 68), (neck[0] - 8, neck[1] - 44)], dark)
        draw_poly(draw, [(neck[0] + 22, neck[1] - 40), (neck[0] + 34, neck[1] - 68), (neck[0] + 8, neck[1] - 44)], dark)
    elif kind == "sage":
        draw_poly(draw, [(neck[0] - 16, neck[1] - 4), (neck[0] + 16, neck[1] - 4), (neck[0] + 12, neck[1] - 36), (neck[0] - 12, neck[1] - 36)], hide)
        draw_poly(draw, [(neck[0] - 22, neck[1] - 28), (neck[0] + 22, neck[1] - 28), (neck[0], neck[1] - 88)], dark)
    elif kind == "harper":
        draw_poly(draw, [(neck[0] - 18, neck[1] - 6), (neck[0] + 18, neck[1] - 6), (neck[0] + 14, neck[1] - 40), (neck[0] - 14, neck[1] - 40)], hide)
        draw_poly(draw, [(neck[0] - 20, neck[1] - 40), (neck[0] + 20, neck[1] - 40), (neck[0] + 16, neck[1] - 56), (neck[0] - 16, neck[1] - 56)], dark)
    elif kind == "bird":
        draw_poly(draw, [(neck[0] - 14, neck[1] - 4), (neck[0] + 10, neck[1] - 8), (neck[0] + 36, neck[1] - 28), (neck[0] + 8, neck[1] - 22), (neck[0] - 10, neck[1] - 36)], hide)
    else:  # demon
        draw_poly(draw, [(neck[0] - 20, neck[1] - 4), (neck[0] + 20, neck[1] - 4), (neck[0] + 16, neck[1] - 40), (neck[0] - 16, neck[1] - 40)], hide)
        draw_poly(draw, [(neck[0] - 16, neck[1] - 40), (neck[0] - 28, neck[1] - 72), (neck[0] - 4, neck[1] - 44)], dark)
        draw_poly(draw, [(neck[0] + 16, neck[1] - 40), (neck[0] + 28, neck[1] - 72), (neck[0] + 4, neck[1] - 44)], dark)

    lsh = rot(j["lsh"], torso_origin, ang["torso"])
    rsh = rot(j["rsh"], torso_origin, ang["torso"])
    lhip = rot(j["lhip"], torso_origin, ang["torso"])
    rhip = rot(j["rhip"], torso_origin, ang["torso"])

    def limb(origin: tuple[float, float], rest: tuple[float, float], swing: float, width: float) -> None:
        tip = rot(rest, origin, swing)
        draw_poly(draw, wedge(origin, tip, width), hide)

    # Rest poses point down/out; swing is added on top.
    limb(lsh, (lsh[0] - 54, lsh[1] + 72), ang["larm"], 13)
    limb(rsh, (rsh[0] + 54, rsh[1] + 72), ang["rarm"], 13)
    limb(lhip, (lhip[0] - 18, lhip[1] + 92), ang["lleg"], 15)
    limb(rhip, (rhip[0] + 18, rhip[1] + 92), ang["rleg"], 15)

    # Props that dance with an arm.
    if kind == "knight":
        hand = rot((rsh[0] + 54, rsh[1] + 72), rsh, ang["rarm"])
        blade = rot((hand[0] + 8, hand[1] - 70), hand, ang["rarm"] * 0.2)
        draw_poly(draw, wedge(hand, blade, 5), dark)
    elif kind == "sage":
        hand = rot((rsh[0] + 54, rsh[1] + 72), rsh, ang["rarm"])
        staff = (hand[0] + 6, hand[1] + 90)
        draw_poly(draw, wedge((hand[0], hand[1] - 80), staff, 4), dark)
    elif kind == "harper":
        hand = rot((lsh[0] - 54, lsh[1] + 72), lsh, ang["larm"])
        draw.arc((int(hand[0] - 18), int(hand[1] - 28), int(hand[0] + 22), int(hand[1] + 22)), 200, 520, fill=dark, width=4)
    elif kind == "demon":
        tail_root = rot((256.0, 310.0), torso_origin, ang["torso"])
        tail_tip = rot((tail_root[0] + 70, tail_root[1] + 20), tail_root, math.sin(clock(frame)) * 0.5)
        draw_poly(draw, wedge(tail_root, tail_tip, 7), hide)
    elif kind == "bride":
        # Skirt wedges that flare with the step.
        flare = 18 + math.sin(clock(frame)) * 10
        hem = [
            (torso[4][0] - flare, 400),
            (256, 318),
            (torso[2][0] + flare, 400),
            (256, 418),
        ]
        draw_poly(draw, hem, hide)
    elif kind == "clown":
        # Ruff — a sawtooth collar.
        for i in range(6):
            a = -0.6 + i * 0.24
            p0 = rot((256, 188), torso_origin, ang["torso"])
            p1 = rot((256 + math.cos(a) * 34, 188 + math.sin(a) * 16 - 10), torso_origin, ang["torso"])
            p2 = rot((256 + math.cos(a + 0.2) * 28, 188 + math.sin(a + 0.2) * 12), torso_origin, ang["torso"])
            draw_poly(draw, [p0, p1, p2], dark)

    return canvas


def paint_hinge(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    canvas = blank()
    draw = ImageDraw.Draw(canvas, "RGBA")
    rgb = METAL[kind]
    t = clock(frame)
    # Brads sit on the shared joint map so any cast still reads as jointed.
    j = joints()
    pulse = 1.0 + 0.08 * math.sin(t)
    for key, (x, y) in j.items():
        if key == "neck":
            continue
        r = 5.5 * pulse
        draw.ellipse((x - r, y - r, x + r, y + r), fill=rgb + (230,))
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(24, 18, 12, 220))
    return canvas


def paint_cutwork(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    canvas = blank()
    draw = ImageDraw.Draw(canvas, "RGBA")
    # Punch holes as light-through-leather, not a walking cancel.
    holes: list[tuple[float, float, float]] = []
    if kind == "dots":
        holes = [(236, 230, 5), (276, 230, 5), (256, 258, 6), (246, 286, 4), (266, 286, 4)]
    elif kind == "stars":
        for cx, cy in ((236, 236), (276, 236), (256, 272)):
            pts = []
            for i in range(5):
                a = -math.pi / 2 + i * math.tau / 5
                pts.append((cx + math.cos(a) * 8, cy + math.sin(a) * 8))
                pts.append((cx + math.cos(a + math.tau / 10) * 3.5, cy + math.sin(a + math.tau / 10) * 3.5))
            draw.polygon([(int(x), int(y)) for x, y in pts], fill=(243, 230, 200, 210))
        return canvas
    elif kind == "diamonds":
        for cx, cy in ((240, 240), (272, 240), (256, 270), (256, 298)):
            draw.polygon([(cx, cy - 7), (cx + 6, cy), (cx, cy + 7), (cx - 6, cy)], fill=(243, 230, 200, 210))
        return canvas
    else:  # vine
        for i in range(5):
            y = 220 + i * 18
            x = 256 + math.sin(clock(frame) * 0.4 + i) * 6
            holes.append((x, y, 3.5))
            holes.append((x - 12, y + 6, 2.5))
            holes.append((x + 12, y + 6, 2.5))
    for x, y, r in holes:
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(243, 230, 200, 210))
    return canvas


def paint_leaf(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    canvas = blank()
    draw = ImageDraw.Draw(canvas, "RGBA")
    gold = (212, 168, 64, 200)
    # Gold on the hide edge — leaf, not a crease score and not a cancel.
    if kind == "rim":
        draw.polygon([(216, 196), (296, 196), (308, 292), (256, 318), (204, 292)], outline=gold)
    elif kind == "tips":
        for box in ((188, 250, 210, 272), (302, 250, 324, 272), (228, 370, 248, 392), (264, 370, 284, 392)):
            draw.ellipse(box, outline=gold, width=2)
    elif kind == "full":
        draw.polygon([(216, 196), (296, 196), (308, 292), (256, 318), (204, 292)], outline=gold)
        draw.arc((228, 128, 284, 184), 200, 340, fill=gold, width=2)
    else:  # dust
        rng = np.random.RandomState(seed_for("leaf"))
        for _ in range(40):
            x = int(rng.randint(180, 332))
            y = int(rng.randint(160, 380))
            draw.point((x, y), fill=gold)
    return canvas


def paint_soot(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    canvas = blank()
    draw = ImageDraw.Draw(canvas, "RGBA")
    t = clock(frame)
    if kind == "motes":
        rng = np.random.RandomState(seed_for("soot", "motes"))
        for i in range(28):
            x = 80 + (rng.random() * 350 + math.sin(t + i) * 8)
            y = 60 + (rng.random() * 380 + math.cos(t * 0.8 + i) * 6)
            r = 1 + int(rng.random() * 2)
            draw.ellipse((x - r, y - r, x + r, y + r), fill=(24, 16, 10, 140))
    elif kind == "ribbon":
        pts = [(40 + i * 18, 90 + math.sin(t + i * 0.35) * 16) for i in range(24)]
        draw.line(pts, fill=(24, 16, 10, 90), width=3)
    elif kind == "haze":
        draw.ellipse((60, 40, 452, 200), fill=(24, 16, 10, 40))
        draw.ellipse((90, 80, 420, 240), fill=(24, 16, 10, 28))
    else:  # spark
        for i in range(10):
            a = t + i * 0.62
            x = 256 + math.cos(a) * (40 + i * 8)
            y = 380 - i * 18 - math.sin(t) * 6
            draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(232, 168, 64, 180))
    return canvas


PAINTERS = {
    "cloth": {k: (lambda kind: (lambda frame, k=kind: paint_cloth(k, frame)))(k) for k in CLOTHS},
    "ember": {k: (lambda kind: (lambda frame, k=kind: paint_ember(k, frame)))(k) for k in EMBERS},
    "cast": {k: (lambda kind: (lambda frame, k=kind: paint_cast(k, frame)))(k) for k in CASTS},
    "hinge": {k: (lambda kind: (lambda frame, k=kind: paint_hinge(k, frame)))(k) for k in HINGES},
    "cutwork": {k: (lambda kind: (lambda frame, k=kind: paint_cutwork(k, frame)))(k) for k in CUTWORKS},
    "leaf": {k: (lambda kind: (lambda frame, k=kind: paint_leaf(k, frame)))(k) for k in LEAFS},
    "soot": {k: (lambda kind: (lambda frame, k=kind: paint_soot(k, frame)))(k) for k in SOOTS},
}

STACK = ("cloth", "ember", "cast", "hinge", "cutwork", "leaf", "soot")

TRAIT_SPEC: dict[str, list[tuple[str, str, int]]] = {
    "cloth": [
        ("parchment", "Parchment Screen", 18),
        ("saffron", "Saffron Screen", 14),
        ("dusk", "Dusk Screen", 12),
        ("smoke", "Smoke Screen", 12),
        ("indigo", "Indigo Screen", 12),
        ("rose", "Rose Screen", 12),
        ("ash", "Ash Screen", 10),
        ("brass", "Brass Screen", 10),
    ],
    "ember": [
        ("oil", "Oil Lamp", 20),
        ("coal", "Coal Glow", 16),
        ("dawn", "Dawn Glow", 16),
        ("hearth", "Hearth Glow", 16),
        ("moon", "Moon Glow", 16),
        ("forge", "Forge Glow", 16),
    ],
    "cast": [
        ("clown", "Clown", 18),
        ("knight", "Knight", 16),
        ("bride", "Bride", 14),
        ("ogre", "Ogre", 14),
        ("sage", "Sage", 12),
        ("harper", "Harper", 10),
        ("bird", "Bird", 8),
        ("demon", "Demon", 8),
    ],
    "hinge": [
        ("none", "No Hinge", 22),
        ("brass", "Brass Brad", 22),
        ("iron", "Iron Brad", 20),
        ("pearl", "Pearl Brad", 18),
        ("rust", "Rust Brad", 18),
    ],
    "cutwork": [
        ("none", "Solid Hide", 26),
        ("dots", "Dot Lace", 20),
        ("stars", "Star Lace", 18),
        ("diamonds", "Diamond Lace", 18),
        ("vine", "Vine Lace", 18),
    ],
    "leaf": [
        ("none", "Bare Hide", 26),
        ("rim", "Gold Rim", 20),
        ("tips", "Gold Tips", 18),
        ("full", "Full Leaf", 18),
        ("dust", "Gold Dust", 18),
    ],
    "soot": [
        ("none", "Clear Air", 24),
        ("motes", "Soot Motes", 20),
        ("ribbon", "Smoke Ribbon", 20),
        ("haze", "Lamp Haze", 18),
        ("spark", "Spark Rise", 18),
    ],
}

SIGNATURES = [
    {"cloth": "parchment", "ember": "oil", "cast": "clown", "hinge": "brass", "cutwork": "dots", "leaf": "rim", "soot": "motes"},
    {"cloth": "dusk", "ember": "coal", "cast": "knight", "hinge": "iron", "cutwork": "none", "leaf": "tips", "soot": "spark"},
    {"cloth": "saffron", "ember": "dawn", "cast": "bride", "hinge": "pearl", "cutwork": "stars", "leaf": "full", "soot": "ribbon"},
    {"cloth": "indigo", "ember": "moon", "cast": "ogre", "hinge": "rust", "cutwork": "diamonds", "leaf": "none", "soot": "haze"},
    {"cloth": "rose", "ember": "hearth", "cast": "sage", "hinge": "brass", "cutwork": "vine", "leaf": "rim", "soot": "none"},
    {"cloth": "brass", "ember": "forge", "cast": "harper", "hinge": "none", "cutwork": "dots", "leaf": "dust", "soot": "motes"},
    {"cloth": "smoke", "ember": "oil", "cast": "bird", "hinge": "pearl", "cutwork": "stars", "leaf": "tips", "soot": "ribbon"},
    {"cloth": "ash", "ember": "coal", "cast": "demon", "hinge": "iron", "cutwork": "none", "leaf": "full", "soot": "spark"},
    {"cloth": "parchment", "ember": "hearth", "cast": "knight", "hinge": "brass", "cutwork": "vine", "leaf": "none", "soot": "haze"},
    {"cloth": "dusk", "ember": "dawn", "cast": "clown", "hinge": "none", "cutwork": "diamonds", "leaf": "dust", "soot": "motes"},
    {"cloth": "saffron", "ember": "moon", "cast": "ogre", "hinge": "pearl", "cutwork": "dots", "leaf": "rim", "soot": "none"},
    {"cloth": "indigo", "ember": "forge", "cast": "bride", "hinge": "rust", "cutwork": "none", "leaf": "tips", "soot": "spark"},
    {"cloth": "rose", "ember": "oil", "cast": "bird", "hinge": "brass", "cutwork": "stars", "leaf": "full", "soot": "ribbon"},
    {"cloth": "brass", "ember": "coal", "cast": "sage", "hinge": "iron", "cutwork": "diamonds", "leaf": "none", "soot": "haze"},
    {"cloth": "smoke", "ember": "hearth", "cast": "demon", "hinge": "pearl", "cutwork": "vine", "leaf": "dust", "soot": "motes"},
    {"cloth": "ash", "ember": "dawn", "cast": "harper", "hinge": "rust", "cutwork": "stars", "leaf": "rim", "soot": "spark"},
]

TRAIT_LABELS = (
    ("cloth", "Cloth"),
    ("ember", "Ember"),
    ("cast", "Cast"),
    ("hinge", "Hinge"),
    ("cutwork", "Cutwork"),
    ("leaf", "Leaf"),
    ("soot", "Soot"),
)

COLLECTION_DESCRIPTION = (
    "Umbra is an 8,888-piece collection of looping shadow-puppet PFP GIFs. "
    "Each shade is stacked from seven plates — cloth, ember, cast, hinge, cutwork, leaf, and soot — "
    "then flattened onto one 12-frame GIF. Leather silhouettes. Brass brads. A lamp that dances with the limbs."
)

COLLECTION_STORY = (
    "Umbra.\n\n"
    "An 8,888-piece collection of looping shadow-puppet PFP GIFs on Robinhood Chain. "
    "Each shade is stacked from seven plates — cloth, ember, cast, hinge, cutwork, leaf, and soot — "
    "then flattened onto one 12-frame GIF. Eight dancing casts: clown, knight, bride, ogre, sage, harper, bird, and demon. "
    "Hinges swing the step. Cutwork lets the lamp through. Gold leaf rides the hide.\n\n"
    "Leather on a woven screen. Not risograph blots. Not origami facets. Not an engraved bust. "
    "The cast stays seated in one envelope. The dance is in the joints. One shared clock.\n\n"
    "Minting free on Robinhood Chain (chain ID 4663). Gas is ETH."
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
        "name": "Umbra",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Eight dancing casts share one envelope; hinges and soot never edit the cast file.",
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
                "name": f"Shade #{index}",
                "image": f"/umbra-preview/{index}.gif",
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
    (SRC_DATA / "umbra-gallery.ts").write_text(
        "export type UmbraSample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const umbraSamples: UmbraSample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def write_ts_traits() -> None:
    blurbs = {
        "cloth": "The lamp screen — parchment, saffron, dusk, smoke, indigo, rose, ash, brass.",
        "ember": "The light behind the hide — oil, coal, dawn, hearth, moon, forge.",
        "cast": "The dancing puppet. Eight casts: clown, knight, bride, ogre, sage, harper, bird, demon.",
        "hinge": "Brads at the joints — brass, iron, pearl, rust — or a seamless hide.",
        "cutwork": "Lace punched through the leather — dots, stars, diamonds, vine — or solid hide.",
        "leaf": "Gold on the edge — rim, tips, full leaf, dust — or bare hide.",
        "soot": "Air in front of the screen — motes, ribbon, haze, spark — or clear air.",
    }
    none_labels = {
        "hinge": "No Hinge",
        "cutwork": "Solid Hide",
        "leaf": "Bare Hide",
        "soot": "Clear Air",
    }
    cats = []
    for key, label in TRAIT_LABELS:
        traits = []
        for trait_id, name, rarity in TRAIT_SPEC[key]:
            if trait_id == "none":
                continue
            traits.append(
                "      { "
                f'id: "{trait_id}", name: "{name}", image: "/umbra-traits/{key}/{trait_id}.png", rarity: {rarity} '
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
    (SRC_DATA / "umbra-traits.ts").write_text(
        "export type UmbraTrait = {\n"
        "  id: string;\n"
        "  name: string;\n"
        "  image?: string;\n"
        "  rarity: number;\n"
        "};\n\n"
        "export type UmbraTraitCategory = {\n"
        f"  id: {ids};\n"
        "  label: string;\n"
        "  blurb: string;\n"
        "  noneLabel?: string;\n"
        "  traits: UmbraTrait[];\n"
        "};\n\n"
        "/** Bump when APNG layers change so the studio does not keep a stale loop. */\n"
        'export const UMBRA_ART_VERSION = "umbra-v1";\n\n'
        "export const UMBRA_FRAMES = 12;\n"
        "export const UMBRA_DURATION_MS = 90;\n\n"
        "export function umbraTraitSrc(path?: string) {\n"
        "  if (!path) return \"\";\n"
        "  return `${path}?v=${UMBRA_ART_VERSION}`;\n"
        "}\n\n"
        "export const umbraTraitCategories: UmbraTraitCategory[] = [\n"
        + ",\n".join(cats)
        + "\n];\n\n"
        'export const noneUmbraTrait: UmbraTrait = { id: "none", name: "None", rarity: 0 };\n\n'
        "export function umbraCategoryById(id: UmbraTraitCategory[\"id\"]) {\n"
        "  const category = umbraTraitCategories.find((item) => item.id === id);\n"
        "  if (!category) throw new Error(`Unknown Umbra trait category: ${id}`);\n"
        "  return category;\n"
        "}\n\n"
        "export function findUmbraTrait(categoryId: UmbraTraitCategory[\"id\"], traitId: string) {\n"
        "  if (traitId === \"none\") return noneUmbraTrait;\n"
        "  return umbraCategoryById(categoryId).traits.find((trait) => trait.id === traitId);\n"
        "}\n\n"
        "export const defaultUmbraSelection = {\n"
        '  cloth: "parchment",\n'
        '  ember: "oil",\n'
        '  cast: "clown",\n'
        '  hinge: "brass",\n'
        '  cutwork: "dots",\n'
        '  leaf: "rim",\n'
        '  soot: "motes",\n'
        "} as const;\n\n"
        "export type UmbraSelection = Record<UmbraTraitCategory[\"id\"], string>;\n\n"
        "export function randomUmbraSelection(): UmbraSelection {\n"
        "  const pick = (category: UmbraTraitCategory) => {\n"
        "    const pool: UmbraTrait[] = category.noneLabel\n"
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
        '    cloth: pick(umbraCategoryById("cloth")),\n'
        '    ember: pick(umbraCategoryById("ember")),\n'
        '    cast: pick(umbraCategoryById("cast")),\n'
        '    hinge: pick(umbraCategoryById("hinge")),\n'
        '    cutwork: pick(umbraCategoryById("cutwork")),\n'
        '    leaf: pick(umbraCategoryById("leaf")),\n'
        '    soot: pick(umbraCategoryById("soot")),\n'
        "  };\n"
        "}\n\n"
        "export function umbraCombinationCount() {\n"
        "  return umbraTraitCategories.reduce((product, category) => {\n"
        "    const extra = category.noneLabel ? 1 : 0;\n"
        "    return product * (category.traits.length + extra);\n"
        "  }, 1);\n"
        "}\n\n"
        "export function umbraSelectionToLayers(selection: UmbraSelection) {\n"
        '  return (["cloth", "ember", "cast", "hinge", "cutwork", "leaf", "soot"] as const)\n'
        "    .map((id) => findUmbraTrait(id, selection[id]))\n"
        "    .filter((trait): trait is UmbraTrait => Boolean(trait?.image))\n"
        "    .map((trait) => umbraTraitSrc(trait.image));\n"
        "}\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array(
        [
            [0.95, 0.90, 0.78],
            [0.91, 0.66, 0.25],
            [0.10, 0.07, 0.03],
            [0.36, 0.16, 0.14],
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
    (META_DIR / "umbra-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "umbra.json").write_text(
        json.dumps(
            {
                "name": "Umbra",
                "symbol": "UMBR",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-umbra.gif",
                "featured_image": "/brand/featured-umbra.jpg",
                "banner_image": "/brand/banner-umbra.png",
                "opensea_banner_image": "/brand/banner-umbra-opensea.jpg",
                "external_link": "/umbra",
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
        (12, 12, SIZE - 13, SIZE - 13), radius=40, outline=(232, 168, 64, 255), width=4
    )
    logo = Image.alpha_composite(logo, rim)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-umbra.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-umbra-loop.png",
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

    save_image(lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-umbra.png", quality=94)
    save_image(lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-umbra-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=28)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=28)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-umbra.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(
        gif_frames,
        BRAND_DIR / "collection-umbra.gif",
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
        print("Writing Umbra brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Umbra shadow-puppet dancers…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
