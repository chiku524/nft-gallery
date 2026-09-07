#!/usr/bin/env python3
"""Paint Noxelle — bent-neon club dancers.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
The figure is glass tubing, not a filled body. Gas blooms behind the bend.
Language: noble-gas fill, wall mounts, transformer brick, club spill.
Not leather puppets. Not sticker cutouts. Not oval-egg bodies. Not musical notes.
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

TRAIT_DIR = ROOT / "public" / "noxelle-traits"
PREVIEW_DIR = ROOT / "public" / "noxelle-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

GAS = {
    "argon": (225, 75, 255),
    "neon": (255, 59, 78),
    "krypton": (200, 255, 232),
    "mercury": (78, 200, 255),
    "helium": (255, 176, 112),
    "xenon": (184, 156, 255),
    "sodium": (255, 204, 51),
    "mix": (93, 255, 194),
}

SPILL = {
    "grape": (80, 28, 120),
    "lagoon": (12, 72, 88),
    "cherry": (120, 24, 56),
    "honey": (120, 72, 16),
    "mint": (24, 96, 72),
    "ice": (32, 56, 120),
}

WALL = {
    "velvet": (22, 8, 28),
    "tile": (16, 18, 28),
    "brick": (32, 14, 18),
    "chrome": (18, 22, 28),
    "alley": (24, 22, 20),
    "booth": (28, 10, 22),
    "parking": (20, 20, 22),
    "glass": (10, 16, 24),
}


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def clock(frame: int) -> float:
    return 2.0 * math.pi * frame / FRAMES


def arr_to_image(rgb: np.ndarray, alpha: np.ndarray | None = None) -> Image.Image:
    h, w = rgb.shape[:2]
    a = np.full((h, w), 255, dtype=np.uint8) if alpha is None else alpha
    stacked = np.dstack([np.clip(rgb, 0, 255).astype(np.uint8), a])
    return Image.fromarray(stacked, "RGBA")


def glow_polylines(
    canvas: Image.Image,
    polylines: list[list[tuple[float, float]]],
    color: tuple[int, int, int],
    core: int = 7,
    halo: int = 28,
    halo_alpha: int = 110,
    hot: tuple[int, int, int] = (255, 252, 240),
) -> None:
    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for pts in polylines:
        if len(pts) < 2:
            continue
        gd.line([(int(x), int(y)) for x, y in pts], fill=(*color, halo_alpha), width=halo, joint="curve")
        sx, sy = pts[0]
        ex, ey = pts[-1]
        r = halo // 2
        gd.ellipse((int(sx - r), int(sy - r), int(sx + r), int(sy + r)), fill=(*color, halo_alpha))
        gd.ellipse((int(ex - r), int(ey - r), int(ex + r), int(ey + r)), fill=(*color, halo_alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=max(4, halo // 4)))
    canvas.alpha_composite(glow)
    draw = ImageDraw.Draw(canvas)
    for pts in polylines:
        if len(pts) < 2:
            continue
        xy = [(int(x), int(y)) for x, y in pts]
        draw.line(xy, fill=(*color, 255), width=core, joint="curve")
        draw.line(xy, fill=(*hot, 230), width=max(2, core // 3), joint="curve")
        sx, sy = xy[0]
        ex, ey = xy[-1]
        cap = max(3, core // 2 + 1)
        for cx, cy in ((sx, sy), (ex, ey)):
            draw.ellipse((cx - cap, cy - cap + 1, cx + cap, cy + cap + 2), fill=(36, 32, 40, 255))
            draw.ellipse((cx - cap + 1, cy - cap, cx + cap - 1, cy + cap - 2), fill=(90, 86, 96, 255))


def sample_curve(fn, n: int = 40) -> list[tuple[float, float]]:
    return [fn(i / (n - 1)) for i in range(n)]


def hairpin(cx: float, cy: float, rx: float, ry: float, swing: float) -> list[tuple[float, float]]:
    pts = []
    for i in range(22):
        a = math.pi * 1.15 + i / 21 * math.pi * 1.7
        pts.append((cx + math.cos(a) * rx + swing, cy + math.sin(a) * ry))
    return pts


def bend_paths(kind: str, frame: int) -> list[list[tuple[float, float]]]:
    t = clock(frame)
    sway = math.sin(t) * 18
    bob = math.sin(t * 2) * 8
    kick = math.sin(t) * 0.55
    cx, cy = 256.0, 248.0 - bob

    if kind == "sway":
        torso = sample_curve(lambda u: (cx + sway * (0.3 + u * 0.7) + math.sin(u * math.pi) * 10, 400 - u * 210))
        left = sample_curve(lambda u: (cx - 18 + sway * 0.4 - u * (70 + math.sin(t) * 22), cy + 40 + u * 70 + math.sin(t + u) * 12))
        right = sample_curve(lambda u: (cx + 18 + sway * 0.4 + u * (70 + math.cos(t) * 18), cy + 36 + u * 64 + math.cos(t + u) * 14))
        leg_l = sample_curve(lambda u: (cx - 12 + sway * 0.2 - u * 28, cy + 90 + u * 118))
        leg_r = sample_curve(lambda u: (cx + 16 + sway * 0.2 + u * 22, cy + 90 + u * 118))
        return [torso, hairpin(cx + sway, cy - 78, 28, 34, math.sin(t) * 4), left, right, leg_l, leg_r]

    if kind == "kick":
        torso = sample_curve(lambda u: (cx + sway * 0.4, 392 - u * 200))
        planted = sample_curve(lambda u: (cx - 8 - u * 16, cy + 88 + u * 122))
        flying = sample_curve(lambda u: (cx + 10 + u * (130 + kick * 40), cy + 70 - u * (40 + kick * 50) + math.sin(u * math.pi) * 18))
        arm_l = sample_curve(lambda u: (cx - 16 - u * 78, cy + 20 - u * 50))
        arm_r = sample_curve(lambda u: (cx + 18 + u * 36, cy + 28 + u * 80))
        return [torso, hairpin(cx, cy - 82, 26, 32, 0), planted, flying, arm_l, arm_r]

    if kind == "spin":
        turns = 1.15 + 0.08 * math.sin(t)
        coil = sample_curve(
            lambda u: (
                cx + math.cos(u * turns * 2 * math.pi + t) * (18 + u * 92),
                400 - u * 250 + math.sin(u * turns * 2 * math.pi + t) * 8,
            ),
            n=56,
        )
        arm = sample_curve(lambda u: (cx + math.cos(t + 1.2) * (40 + u * 90), cy - 10 + math.sin(t + 1.2) * (20 + u * 40)))
        return [coil, arm]

    if kind == "dip":
        arc = sample_curve(
            lambda u: (
                130 + u * 250 + sway * 0.3,
                330 - math.sin(u * math.pi) * (150 + bob * 0.6),
            ),
            n=44,
        )
        arm = sample_curve(lambda u: (cx - 80 + sway + u * 30, 210 - u * 90))
        trail = sample_curve(lambda u: (cx + 90 + sway + u * 40, 230 + u * 110))
        return [arc, arm, trail]

    if kind == "wave":
        torso = sample_curve(lambda u: (cx + sway * 0.5, 398 - u * 206))
        wave = sample_curve(
            lambda u: (
                cx + 22 + u * 120,
                cy + 8 - u * 130 + math.sin(u * 3 * math.pi + t) * 22,
            ),
            n=36,
        )
        arm_l = sample_curve(lambda u: (cx - 20 - u * 72, cy + 30 + u * 70))
        leg_l = sample_curve(lambda u: (cx - 14 - u * 24, cy + 92 + u * 116))
        leg_r = sample_curve(lambda u: (cx + 18 + u * 20, cy + 92 + u * 116))
        return [torso, hairpin(cx + sway * 0.4, cy - 80, 27, 33, math.sin(t) * 3), wave, arm_l, leg_l, leg_r]

    if kind == "hop":
        lift = 18 + abs(math.sin(t)) * 36
        torso = sample_curve(lambda u: (cx, 410 - lift - u * (190 - lift * 0.25)))
        spring_l = sample_curve(lambda u: (cx - 10 - math.sin(u * math.pi) * 36, cy + 70 + lift * 0.2 + u * (90 - lift * 0.4)))
        spring_r = sample_curve(lambda u: (cx + 12 + math.sin(u * math.pi) * 36, cy + 70 + lift * 0.2 + u * (90 - lift * 0.4)))
        arms = sample_curve(lambda u: (cx - 70 + u * 140, cy + 10 - abs(math.sin(t)) * 40 - math.sin(u * math.pi) * 18))
        return [torso, hairpin(cx, cy - 70 - lift * 0.35, 24, 28, 0), spring_l, spring_r, arms]

    if kind == "point":
        lean = 38 + math.sin(t) * 10
        torso = sample_curve(lambda u: (cx - 40 + u * lean * 2.1, 400 - u * 215))
        arm = sample_curve(lambda u: (cx + lean * 0.4 + u * 150, cy - 20 - u * 90))
        back = sample_curve(lambda u: (cx - 30 - u * 80, cy + 24 + u * 40))
        leg = sample_curve(lambda u: (cx - 36 - u * 20, cy + 88 + u * 118))
        return [torso, hairpin(cx + lean * 0.85, cy - 86, 24, 30, 2), arm, back, leg]

    # split
    torso = sample_curve(lambda u: (cx, 360 - u * 170))
    left = sample_curve(lambda u: (cx - u * (150 + math.sin(t) * 12), cy + 70 + u * 40 + math.sin(u * math.pi) * 16))
    right = sample_curve(lambda u: (cx + u * (150 + math.cos(t) * 12), cy + 70 + u * 40 + math.sin(u * math.pi) * 16))
    up = sample_curve(lambda u: (cx + math.sin(t) * 10, cy - 20 - u * 110))
    return [torso, hairpin(cx, cy - 88, 26, 30, math.sin(t) * 5), left, right, up]


def paint_wall(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    yy, xx = np.mgrid[0:SIZE, 0:SIZE]
    base = np.array(WALL[kind], dtype=np.float32)
    rgb = np.broadcast_to(base, (SIZE, SIZE, 3)).copy()
    if kind == "velvet":
        nap = 10 * np.sin(xx / 6.5 + yy / 48.0) + 4 * np.sin(yy / 14.0 + t)
        rgb += nap[..., None]
        rgb[..., 0] += 8 * (yy / SIZE)
    elif kind == "tile":
        grout = ((xx % 44) < 3) | ((yy % 56) < 3)
        rgb[grout] = (8, 9, 14)
        rgb += 6 * np.sin(xx / 44.0)[..., None]
    elif kind == "brick":
        row = (yy // 28) % 2
        grout = ((xx + row * 22) % 44 < 3) | ((yy % 28) < 3)
        rgb[grout] = (18, 10, 12)
        rgb += ((xx // 44 + yy // 28) % 3)[..., None] * 4
    elif kind == "chrome":
        band = 28 + 36 * (0.5 + 0.5 * np.sin(xx / 16.0 + t * 0.25))
        rgb[..., :] = np.clip(np.stack([band * 0.7, band * 0.8, band + 8], axis=-1), 0, 255)
        rgb[yy > 400] *= 0.55
    elif kind == "alley":
        rgb += ((xx // 80 + yy // 110) % 2)[..., None] * 6
        posters = ((xx > 70) & (xx < 170) & (yy > 80) & (yy < 210)) | ((xx > 300) & (xx < 430) & (yy > 140) & (yy < 280))
        rgb[posters] = (40, 18, 48)
    elif kind == "booth":
        diamond = (np.abs((xx % 64) - 32) + np.abs((yy % 48) - 24)) < 18
        rgb[diamond] = (38, 12, 30)
        rgb += 5 * np.sin(yy / 48.0)[..., None]
    elif kind == "parking":
        rgb += 3 * np.sin(xx / 90.0)[..., None]
        line = (yy > 430) & (yy < 446) & (xx > 40) & (xx < 470) & ((xx // 28) % 2 == 0)
        rgb[line] = (210, 180, 40)
    else:
        streak = np.clip(np.sin((xx * 0.04) + (yy * 0.2) + t) * 18, 0, 30)
        rgb[..., 2] += streak
        rgb[..., 1] += streak * 0.4
        drip = ((xx % 37) < 2) & (yy < 220 + 40 * np.sin(xx / 40.0))
        rgb[drip] = np.clip(rgb[drip] + 18, 0, 255)
    rgb += 3 * np.sin(t + yy / 80.0)[..., None]
    return arr_to_image(rgb)


def paint_spill(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    color = SPILL[kind]
    layer = blank()
    d = ImageDraw.Draw(layer)
    pulse = 18 + int(10 * math.sin(t * 2))
    d.ellipse((40, 390, 472, 500 + pulse), fill=(*color, 90))
    d.ellipse((90, -40, 422, 160), fill=(*color, 50))
    return layer.filter(ImageFilter.GaussianBlur(radius=18))


def paint_gas(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    color = GAS[kind]
    layer = blank()
    d = ImageDraw.Draw(layer)
    pulse = int(12 * math.sin(t * 2))
    d.ellipse((90 - pulse, 70 - pulse, 422 + pulse, 430 + pulse), fill=(*color, 70))
    d.ellipse((150, 120, 362, 340), fill=(*color, 40))
    return layer.filter(ImageFilter.GaussianBlur(radius=22))


def paint_bend(kind: str, frame: int) -> Image.Image:
    layer = blank()
    glow_polylines(layer, bend_paths(kind, frame), (236, 244, 255), core=8, halo=26, halo_alpha=80)
    return layer


def paint_clip(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    layer = blank()
    d = ImageDraw.Draw(layer)
    metal = (70, 68, 78, 255)
    dark = (28, 26, 32, 255)
    if kind == "brick":
        d.rounded_rectangle((28, 400, 118, 478), radius=8, fill=dark)
        d.rounded_rectangle((36, 410, 110, 468), radius=6, fill=metal)
        for i in range(3):
            x = 48 + i * 22
            d.rectangle((x, 422, x + 10, 456), fill=(20, 18, 24, 255))
        d.line((118, 438, 150, 430), fill=metal, width=6)
    elif kind == "conduit":
        d.arc((12, 40, 140, 200), 180, 270, fill=metal, width=10)
        d.line((20, 120, 20, 460), fill=metal, width=10)
        d.ellipse((12, 452, 32, 472), fill=dark)
    elif kind == "clips":
        for i, (x, y) in enumerate(((168, 96), (344, 108), (210, 390), (318, 398))):
            wobble = math.sin(t + i) * 2
            d.rectangle((x - 8, y - 6 + wobble, x + 8, y + 10 + wobble), fill=metal)
            d.rectangle((x - 3, y - 12 + wobble, x + 3, y + 14 + wobble), fill=dark)
    else:
        d.line((40, 460, 140, 420, 240, 460, 340, 418, 440, 458), fill=metal, width=8, joint="curve")
        for x, y in ((40, 460), (140, 420), (240, 460), (340, 418), (440, 458)):
            d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=dark)
    return layer


def paint_badge(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    layer = blank()
    bx, by = 392.0, 96.0 + math.sin(t * 2) * 8
    color = (255, 230, 160) if kind in {"moon", "star"} else (255, 120, 170) if kind == "heart" else (160, 220, 255)
    if kind == "bolt":
        color = (255, 230, 90)
    paths: list[list[tuple[float, float]]]
    if kind == "moon":
        paths = [
            sample_curve(lambda u: (bx + math.cos(u * 1.6 * math.pi + 0.6) * 28, by + math.sin(u * 1.6 * math.pi + 0.6) * 34), n=24)
        ]
    elif kind == "bolt":
        paths = [[(bx - 8, by - 28), (bx + 10, by - 4), (bx - 6, by - 2), (bx + 12, by + 30)]]
    elif kind == "heart":
        paths = [
            sample_curve(
                lambda u: (
                    bx + 26 * math.sin(u * 2 * math.pi) ** 3,
                    by - 8 - 10 * (2 * math.cos(u * 2 * math.pi) - math.cos(2 * u * 2 * math.pi) - 0.2 * math.cos(3 * u * 2 * math.pi)),
                ),
                n=36,
            )
        ]
    elif kind == "star":
        pts = []
        for i in range(11):
            a = -math.pi / 2 + i * math.pi / 5
            r = 26 if i % 2 == 0 else 11
            pts.append((bx + math.cos(a) * r, by + math.sin(a) * r))
        paths = [pts]
    else:
        paths = [
            sample_curve(lambda u: (bx + math.cos(u * 2 * math.pi) * 22, by + math.sin(u * 2 * math.pi) * 22), n=28),
            [(bx - 4, by + 4), (bx - 4, by - 26), (bx + 14, by - 18)],
        ]
    glow_polylines(layer, paths, color, core=5, halo=16, halo_alpha=120)
    return layer


def paint_mote(kind: str, frame: int) -> Image.Image:
    t = clock(frame)
    layer = blank()
    d = ImageDraw.Draw(layer)
    rng = np.random.RandomState({"spark": 11, "moth": 23, "dust": 47, "tick": 61}[kind])
    if kind == "spark":
        for i in range(14):
            ang = t * 1.4 + i * 0.7
            x = 256 + math.cos(ang) * (90 + (i % 5) * 18)
            y = 240 + math.sin(ang * 1.3) * (70 + (i % 4) * 16)
            r = 2 + (i % 3)
            d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 250, 210, 200))
    elif kind == "moth":
        for i, (ox, oy) in enumerate(((-110, -80), (120, -40), (90, 70))):
            x = 256 + ox + math.sin(t * 2 + i) * 16
            y = 220 + oy + math.cos(t * 2 + i) * 10
            wing = 10 + int(6 * abs(math.sin(t * 4 + i)))
            d.ellipse((x - wing, y - 5, x + 2, y + 5), fill=(230, 220, 200, 140))
            d.ellipse((x - 2, y - 5, x + wing, y + 5), fill=(230, 220, 200, 140))
    elif kind == "dust":
        xs = rng.randint(40, 470, 28)
        ys = rng.randint(40, 470, 28)
        for i, (x, y) in enumerate(zip(xs, ys)):
            yy = (int(y) + int(frame * 3 + i * 7)) % 480 + 16
            d.point((int(x), yy), fill=(220, 210, 255, 160))
            d.ellipse((int(x), yy, int(x) + 2, yy + 2), fill=(220, 210, 255, 90))
    else:
        for i in range(8):
            on = (frame + i) % 6 < 2
            if not on:
                continue
            x = 80 + i * 48
            y = 70 + (i % 3) * 120
            d.rectangle((x, y, x + 7, y + 3), fill=(255, 255, 240, 220))
    return layer


PAINTERS = {
    "wall": {k: (lambda kind: (lambda frame, k=kind: paint_wall(k, frame)))(k) for k in WALL},
    "spill": {k: (lambda kind: (lambda frame, k=kind: paint_spill(k, frame)))(k) for k in SPILL},
    "gas": {k: (lambda kind: (lambda frame, k=kind: paint_gas(k, frame)))(k) for k in GAS},
    "bend": {
        k: (lambda kind: (lambda frame, k=kind: paint_bend(k, frame)))(k)
        for k in ("sway", "kick", "spin", "dip", "wave", "hop", "point", "split")
    },
    "clip": {k: (lambda kind: (lambda frame, k=kind: paint_clip(k, frame)))(k) for k in ("brick", "conduit", "clips", "daisy")},
    "badge": {k: (lambda kind: (lambda frame, k=kind: paint_badge(k, frame)))(k) for k in ("moon", "bolt", "heart", "star", "disc")},
    "mote": {k: (lambda kind: (lambda frame, k=kind: paint_mote(k, frame)))(k) for k in ("spark", "moth", "dust", "tick")},
}

STACK = ("wall", "spill", "gas", "bend", "clip", "badge", "mote")

TRAIT_SPEC: dict[str, list[tuple[str, str, int]]] = {
    "wall": [
        ("velvet", "Velvet Wall", 16),
        ("tile", "Tile Wall", 14),
        ("brick", "Brick Wall", 14),
        ("chrome", "Chrome Wall", 12),
        ("alley", "Alley Wall", 12),
        ("booth", "Booth Wall", 12),
        ("parking", "Parking Wall", 10),
        ("glass", "Glass Wall", 10),
    ],
    "spill": [
        ("grape", "Grape Spill", 18),
        ("lagoon", "Lagoon Spill", 17),
        ("cherry", "Cherry Spill", 17),
        ("honey", "Honey Spill", 16),
        ("mint", "Mint Spill", 16),
        ("ice", "Ice Spill", 16),
    ],
    "gas": [
        ("argon", "Argon", 16),
        ("neon", "Neon", 16),
        ("krypton", "Krypton", 14),
        ("mercury", "Mercury", 14),
        ("helium", "Helium", 12),
        ("xenon", "Xenon", 12),
        ("sodium", "Sodium", 8),
        ("mix", "Shop Mix", 8),
    ],
    "bend": [
        ("sway", "Sway Bend", 18),
        ("kick", "Kick Bend", 16),
        ("wave", "Wave Bend", 14),
        ("hop", "Hop Bend", 14),
        ("point", "Point Bend", 12),
        ("dip", "Dip Bend", 10),
        ("spin", "Spin Bend", 8),
        ("split", "Split Bend", 8),
    ],
    "clip": [
        ("none", "No Clip", 24),
        ("brick", "Transformer Brick", 22),
        ("conduit", "Conduit Run", 20),
        ("clips", "Wall Clips", 18),
        ("daisy", "Daisy Chain", 16),
    ],
    "badge": [
        ("none", "No Badge", 28),
        ("moon", "Moon Badge", 16),
        ("bolt", "Bolt Badge", 16),
        ("heart", "Heart Badge", 14),
        ("star", "Star Badge", 14),
        ("disc", "Disc Badge", 12),
    ],
    "mote": [
        ("none", "Clear Air", 26),
        ("spark", "Spark Motes", 20),
        ("moth", "Night Moths", 18),
        ("dust", "Dust Drift", 18),
        ("tick", "Tick Flicker", 18),
    ],
}

SIGNATURES = [
    {"wall": "velvet", "spill": "grape", "gas": "argon", "bend": "sway", "clip": "brick", "badge": "moon", "mote": "spark"},
    {"wall": "tile", "spill": "lagoon", "gas": "mercury", "bend": "kick", "clip": "conduit", "badge": "none", "mote": "moth"},
    {"wall": "brick", "spill": "cherry", "gas": "neon", "bend": "wave", "clip": "clips", "badge": "bolt", "mote": "tick"},
    {"wall": "chrome", "spill": "ice", "gas": "krypton", "bend": "spin", "clip": "none", "badge": "star", "mote": "dust"},
    {"wall": "alley", "spill": "honey", "gas": "sodium", "bend": "point", "clip": "daisy", "badge": "disc", "mote": "none"},
    {"wall": "booth", "spill": "mint", "gas": "mix", "bend": "hop", "clip": "brick", "badge": "heart", "mote": "spark"},
    {"wall": "parking", "spill": "grape", "gas": "helium", "bend": "dip", "clip": "conduit", "badge": "moon", "mote": "moth"},
    {"wall": "glass", "spill": "lagoon", "gas": "xenon", "bend": "split", "clip": "clips", "badge": "none", "mote": "tick"},
    {"wall": "velvet", "spill": "cherry", "gas": "neon", "bend": "kick", "clip": "none", "badge": "bolt", "mote": "dust"},
    {"wall": "tile", "spill": "honey", "gas": "argon", "bend": "wave", "clip": "daisy", "badge": "star", "mote": "spark"},
    {"wall": "brick", "spill": "mint", "gas": "mercury", "bend": "sway", "clip": "brick", "badge": "none", "mote": "none"},
    {"wall": "chrome", "spill": "grape", "gas": "mix", "bend": "hop", "clip": "conduit", "badge": "disc", "mote": "moth"},
    {"wall": "alley", "spill": "ice", "gas": "krypton", "bend": "point", "clip": "clips", "badge": "heart", "mote": "tick"},
    {"wall": "booth", "spill": "lagoon", "gas": "helium", "bend": "spin", "clip": "none", "badge": "moon", "mote": "dust"},
    {"wall": "parking", "spill": "cherry", "gas": "sodium", "bend": "split", "clip": "brick", "badge": "bolt", "mote": "spark"},
    {"wall": "glass", "spill": "honey", "gas": "xenon", "bend": "dip", "clip": "daisy", "badge": "star", "mote": "moth"},
]

TRAIT_LABELS = (
    ("wall", "Wall"),
    ("spill", "Spill"),
    ("gas", "Gas"),
    ("bend", "Bend"),
    ("clip", "Clip"),
    ("badge", "Badge"),
    ("mote", "Mote"),
)

COLLECTION_DESCRIPTION = (
    "Noxelle is a 10,000-piece collection of looping neon-tube PFP GIFs. "
    "Each sign is stacked from seven plates — wall, spill, gas, bend, clip, badge, and mote — "
    "then flattened onto one 12-frame GIF. Bent glass. Noble gas. A dancer that is the tube."
)

COLLECTION_STORY = (
    "Noxelle.\n\n"
    "A 10,000-piece collection of looping neon-tube PFP GIFs on Robinhood Chain. "
    "Each sign is stacked from seven plates — wall, spill, gas, bend, clip, badge, and mote — "
    "then flattened onto one 12-frame GIF. Eight bends: sway, kick, wave, hop, point, dip, spin, and split. "
    "Argon, neon, krypton, mercury. Clips hold the glass. Spill stains the club wall.\n\n"
    "Bent tubing, not a filled body. No sticker edge. No egg. Not a shadow puppet. Not a musical note. "
    "The dancer stays seated on one envelope. The dance is the bend. One shared clock.\n\n"
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
        "name": "Noxelle",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Eight tube bends share one envelope; clips and motes never edit the bend file.",
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
                "name": f"Tube #{index}",
                "image": f"/noxelle-preview/{index}.gif",
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
    (SRC_DATA / "noxelle-gallery.ts").write_text(
        "export type NoxelleSample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const noxelleSamples: NoxelleSample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def write_ts_traits() -> None:
    blurbs = {
        "wall": "The club surface — velvet, tile, brick, chrome, alley, booth, parking, glass.",
        "spill": "Color on the floor and ceiling — grape, lagoon, cherry, honey, mint, ice.",
        "gas": "The noble fill behind the glass — argon, neon, krypton, mercury, helium, xenon, sodium, shop mix.",
        "bend": "The dancer is the tube. Eight bends: sway, kick, wave, hop, point, dip, spin, split.",
        "clip": "Hardware that holds the glass — transformer, conduit, clips, daisy chain — or bare wall.",
        "badge": "A second small sign — moon, bolt, heart, star, disc — or none.",
        "mote": "Air in front of the tube — spark, moth, dust, tick — or clear air.",
    }
    none_labels = {
        "clip": "No Clip",
        "badge": "No Badge",
        "mote": "Clear Air",
    }
    cats = []
    for key, label in TRAIT_LABELS:
        traits = []
        for trait_id, name, rarity in TRAIT_SPEC[key]:
            if trait_id == "none":
                continue
            traits.append(
                "      { "
                f'id: "{trait_id}", name: "{name}", image: "/noxelle-traits/{key}/{trait_id}.png", rarity: {rarity} '
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
    (SRC_DATA / "noxelle-traits.ts").write_text(
        "export type NoxelleTrait = {\n"
        "  id: string;\n"
        "  name: string;\n"
        "  image?: string;\n"
        "  rarity: number;\n"
        "};\n\n"
        "export type NoxelleTraitCategory = {\n"
        f"  id: {ids};\n"
        "  label: string;\n"
        "  blurb: string;\n"
        "  noneLabel?: string;\n"
        "  traits: NoxelleTrait[];\n"
        "};\n\n"
        "/** Bump when APNG layers change so the studio does not keep a stale loop. */\n"
        'export const NOXELLE_ART_VERSION = "noxelle-v1";\n\n'
        "export const NOXELLE_FRAMES = 12;\n"
        "export const NOXELLE_DURATION_MS = 90;\n\n"
        "export function noxelleTraitSrc(path?: string) {\n"
        "  if (!path) return \"\";\n"
        "  return `${path}?v=${NOXELLE_ART_VERSION}`;\n"
        "}\n\n"
        "export const noxelleTraitCategories: NoxelleTraitCategory[] = [\n"
        + ",\n".join(cats)
        + "\n];\n\n"
        'export const noneNoxelleTrait: NoxelleTrait = { id: "none", name: "None", rarity: 0 };\n\n'
        "export function noxelleCategoryById(id: NoxelleTraitCategory[\"id\"]) {\n"
        "  const category = noxelleTraitCategories.find((item) => item.id === id);\n"
        "  if (!category) throw new Error(`Unknown Noxelle trait category: ${id}`);\n"
        "  return category;\n"
        "}\n\n"
        "export function findNoxelleTrait(categoryId: NoxelleTraitCategory[\"id\"], traitId: string) {\n"
        "  if (traitId === \"none\") return noneNoxelleTrait;\n"
        "  return noxelleCategoryById(categoryId).traits.find((trait) => trait.id === traitId);\n"
        "}\n\n"
        "export const defaultNoxelleSelection = {\n"
        '  wall: "velvet",\n'
        '  spill: "grape",\n'
        '  gas: "argon",\n'
        '  bend: "sway",\n'
        '  clip: "brick",\n'
        '  badge: "moon",\n'
        '  mote: "spark",\n'
        "} as const;\n\n"
        "export type NoxelleSelection = Record<NoxelleTraitCategory[\"id\"], string>;\n\n"
        "export function randomNoxelleSelection(): NoxelleSelection {\n"
        "  const pick = (category: NoxelleTraitCategory) => {\n"
        "    const pool: NoxelleTrait[] = category.noneLabel\n"
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
        '    wall: pick(noxelleCategoryById("wall")),\n'
        '    spill: pick(noxelleCategoryById("spill")),\n'
        '    gas: pick(noxelleCategoryById("gas")),\n'
        '    bend: pick(noxelleCategoryById("bend")),\n'
        '    clip: pick(noxelleCategoryById("clip")),\n'
        '    badge: pick(noxelleCategoryById("badge")),\n'
        '    mote: pick(noxelleCategoryById("mote")),\n'
        "  };\n"
        "}\n\n"
        "export function noxelleCombinationCount() {\n"
        "  return noxelleTraitCategories.reduce((product, category) => {\n"
        "    const extra = category.noneLabel ? 1 : 0;\n"
        "    return product * (category.traits.length + extra);\n"
        "  }, 1);\n"
        "}\n\n"
        "export function noxelleSelectionToLayers(selection: NoxelleSelection) {\n"
        '  return (["wall", "spill", "gas", "bend", "clip", "badge", "mote"] as const)\n'
        "    .map((id) => findNoxelleTrait(id, selection[id]))\n"
        "    .filter((trait): trait is NoxelleTrait => Boolean(trait?.image))\n"
        "    .map((trait) => noxelleTraitSrc(trait.image));\n"
        "}\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array(
        [
            [0.06, 0.03, 0.10],
            [0.35, 0.08, 0.42],
            [0.04, 0.22, 0.28],
            [0.88, 0.29, 1.0],
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
    (META_DIR / "noxelle-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "noxelle.json").write_text(
        json.dumps(
            {
                "name": "Noxelle",
                "symbol": "NOXL",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-noxelle.gif",
                "featured_image": "/brand/featured-noxelle.jpg",
                "banner_image": "/brand/banner-noxelle.png",
                "opensea_banner_image": "/brand/banner-noxelle-opensea.jpg",
                "external_link": "/noxelle",
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
        (12, 12, SIZE - 13, SIZE - 13), radius=40, outline=(225, 75, 255, 255), width=4
    )
    logo = Image.alpha_composite(logo, rim)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-noxelle.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-noxelle-loop.png",
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

    save_image(lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-noxelle.png", quality=94)
    save_image(lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-noxelle-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=28)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=28)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-noxelle.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(
        gif_frames,
        BRAND_DIR / "collection-noxelle.gif",
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
        print("Writing Noxelle brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Noxelle neon-tube dancers…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
