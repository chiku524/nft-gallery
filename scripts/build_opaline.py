#!/usr/bin/env python3
"""Paint Opaline — smoked-glass saltwater fish with iridescent film.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
The fish is seated: no bounce, no hover. Light walks the facets.
Vapor hangs in the room. Sheen hue-shifts. Regard inclusions dim.

Look: eight crystal reef fish — parrotfish, blue marlin, queen angelfish,
lionfish, green moray, triggerfish, seahorse, manta. Species glass, not
charcoal, not stickers, not an egg body. Dichroic film. Platinum jewelry.
Editorial studio rooms.
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

GIF_COLORS = 256
GIF_DITHER = Image.Dither.NONE

TRAIT_DIR = ROOT / "public" / "opaline-traits"
PREVIEW_DIR = ROOT / "public" / "opaline-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

CX = 256.0

ATELIERS = ("obsidian", "slate", "dusk", "ivory", "mercury", "wine", "brine", "quartz")
VAPORS = ("none", "mist", "mote", "ribbon", "disc", "plume", "well")
CASTS = ("parrot", "marlin", "angel", "lion", "moray", "trigger", "seahorse", "manta")
SHEENS = ("none", "oil", "aurora", "rose", "peacock", "quicksilver", "prism")
REGARDS = ("quiet", "bloom", "slit", "twin", "void", "gleam")
CRESTS = ("none", "band", "shard", "arc", "spine", "diadem")
CLASPS = ("none", "bar", "drop", "torque", "pin", "coil")

CAST_RGB = {
    "parrot": (56, 188, 156),
    "marlin": (168, 196, 220),
    "angel": (42, 86, 196),
    "lion": (220, 198, 164),
    "moray": (78, 118, 68),
    "trigger": (214, 172, 58),
    "seahorse": (204, 138, 62),
    "manta": (34, 38, 50),
}

ACCENT_RGB = {
    "parrot": (236, 92, 168),
    "marlin": (28, 72, 156),
    "angel": (232, 196, 48),
    "lion": (132, 44, 56),
    "moray": (176, 152, 56),
    "trigger": (44, 44, 48),
    "seahorse": (236, 198, 118),
    "manta": (228, 230, 234),
}

SHEEN_HUE = {
    "oil": 210.0,
    "aurora": 140.0,
    "rose": 18.0,
    "peacock": 175.0,
    "quicksilver": 205.0,
    "prism": 280.0,
}

ATELIER_WASH = {
    "obsidian": ((8, 8, 10), (22, 22, 26), (14, 14, 16)),
    "slate": ((48, 52, 58), (92, 98, 106), (36, 40, 46)),
    "dusk": ((14, 16, 36), (42, 36, 72), (10, 12, 28)),
    "ivory": ((214, 212, 208), (236, 234, 230), (188, 186, 182)),
    "mercury": ((78, 82, 88), (168, 174, 182), (52, 56, 62)),
    "wine": ((36, 12, 20), (78, 24, 36), (22, 8, 14)),
    "brine": ((8, 28, 32), (22, 64, 68), (6, 20, 24)),
    "quartz": ((168, 164, 170), (208, 202, 208), (132, 128, 136)),
}


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def clock(frame: int) -> float:
    return frame / FRAMES * math.tau


def light_vec(frame: int) -> tuple[float, float]:
    t = clock(frame)
    return math.cos(t) * 0.85, -0.35 + math.sin(t) * 0.55


def hue_rgb(h: np.ndarray, s: float, v: float) -> np.ndarray:
    h = np.mod(h, 360.0) / 60.0
    i = np.floor(h).astype(np.int32)
    f = h - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    r = np.choose(i % 6, [v, q, p, p, t, v])
    g = np.choose(i % 6, [t, v, v, q, p, p])
    b = np.choose(i % 6, [p, p, t, v, v, q])
    return np.stack([r, g, b], axis=-1)


def glass_color(kind: str, role: str, index: int, frame: int) -> tuple[int, int, int]:
    if kind == "parrot":
        base = {"beak": 28.0, "face": 168.0, "facet": 200.0, "body": 130.0, "fin": 300.0, "neck": 150.0}.get(role, 90.0)
        h = (base + index * 23.0 + frame * 7.0) % 360.0
        sat = 0.42 if role == "beak" else 0.62
        val = 0.86 if role != "beak" else 0.78
        c = hue_rgb(np.array([h]), sat, val)[0] * 255.0
        return (int(c[0]), int(c[1]), int(c[2]))
    body = CAST_RGB[kind]
    accent = ACCENT_RGB[kind]
    if role in ("sail", "stripe", "spine", "crown", "accent", "horn"):
        return accent
    if role == "bill":
        return (208, 216, 226)
    if role == "belly":
        return accent if kind == "manta" else tuple(min(255, c + 36) for c in body)
    if role == "beak" and kind == "seahorse":
        return accent
    return body


def poly_mask(points: list[tuple[float, float]]) -> np.ndarray:
    layer = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(layer).polygon([(int(round(x)), int(round(y))) for x, y in points], fill=255)
    return np.asarray(layer, dtype=np.uint8)


def rim_mask(mask: np.ndarray, width: int = 2) -> np.ndarray:
    solid = mask > 40
    eroded = solid.copy()
    for _ in range(width):
        eroded = (
            eroded
            & np.roll(eroded, 1, 0)
            & np.roll(eroded, -1, 0)
            & np.roll(eroded, 1, 1)
            & np.roll(eroded, -1, 1)
        )
    return solid & ~eroded


def composite_arr(base: np.ndarray, add: np.ndarray) -> np.ndarray:
    src_a = add[..., 3:4].astype(np.float32) / 255.0
    dst_a = base[..., 3:4].astype(np.float32) / 255.0
    out_a = src_a + dst_a * (1.0 - src_a)
    out_rgb = add[..., :3].astype(np.float32) * src_a + base[..., :3].astype(np.float32) * dst_a * (1.0 - src_a)
    safe = np.maximum(out_a, 1e-6)
    rgb = np.clip(out_rgb / safe, 0, 255)
    alpha = np.clip(out_a * 255.0, 0, 255)
    return np.concatenate([rgb, alpha], axis=-1).astype(np.uint8)


def pour_glass(
    canvas: np.ndarray,
    mask: np.ndarray,
    rgb: tuple[int, int, int],
    light: tuple[float, float],
    frame: int,
    alpha: float,
    caustic_gain: float = 0.16,
    rim: bool = False,
) -> None:
    ys, xs = np.nonzero(mask > 20)
    if xs.size == 0:
        return
    coverage = mask[ys, xs].astype(np.float32) / 255.0
    mx = float(xs.mean())
    my = float(ys.mean())
    dx = (xs.astype(np.float32) - mx) / 92.0
    dy = (ys.astype(np.float32) - my) / 92.0
    shade = 0.46 + 0.48 * np.clip(dx * light[0] - dy * light[1], -0.45, 1.0)
    t = clock(frame)
    cx = math.cos(t) * 0.72
    cy = math.sin(t * 0.85) * 0.48
    caustic = caustic_gain * np.exp(-((dx - cx) ** 2 + (dy - cy) ** 2) / 0.28)
    streak = 0.12 * np.exp(-((dx * 0.35 + dy * 1.4 - math.sin(t) * 0.4) ** 2) / 0.08)
    lum = np.clip(shade + caustic + streak, 0.22, 1.38)
    color = np.array(rgb, dtype=np.float32) * lum[:, None]
    color = np.clip(color, 0, 255)
    a = np.clip(alpha * coverage, 0, 255)
    add = np.zeros((SIZE, SIZE, 4), dtype=np.uint8)
    add[ys, xs, 0] = color[:, 0].astype(np.uint8)
    add[ys, xs, 1] = color[:, 1].astype(np.uint8)
    add[ys, xs, 2] = color[:, 2].astype(np.uint8)
    add[ys, xs, 3] = a.astype(np.uint8)
    if rim:
        edge = rim_mask(mask, 2)
        ey, ex = np.nonzero(edge)
        if ex.size:
            facing = np.clip((ex.astype(np.float32) - mx) / 80.0 * light[0] - (ey.astype(np.float32) - my) / 80.0 * light[1], 0.0, 1.0)
            lift = 0.25 + 0.75 * facing
            add[ey, ex, :3] = np.clip(
                add[ey, ex, :3].astype(np.float32) * (1.0 - 0.35 * lift[:, None]) + 210 * lift[:, None],
                0,
                255,
            ).astype(np.uint8)
            add[ey, ex, 3] = np.maximum(add[ey, ex, 3], (90 + 90 * lift).astype(np.uint8))
    canvas[:] = composite_arr(canvas, add)


# Regard sits on one eye line. Crest and clasp overlay the crown and throat.
# Nothing else is shared — each cast is its own saltwater fish.
EYE_L = (220.0, 184.0)
EYE_R = (292.0, 184.0)
SHEEN_FACE = [(214, 140), (298, 140), (316, 184), (300, 220), (256, 236), (212, 220), (196, 184)]
SHEEN_THROAT = [(242, 280), (270, 280), (276, 340), (236, 340)]


def mirror(poly: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(512.0 - x, y) for x, y in poly]


def pair(poly: list[tuple[float, float]], alpha: int, rim: bool = True) -> list[tuple[list[tuple[float, float]], int, bool]]:
    return [(poly, alpha, rim), (mirror(poly), alpha, rim)]


def face_of(kind: str) -> list[tuple[float, float]]:
    """Fish heads. Wide enough to hold the shared eyes, never a mannequin hex."""
    if kind == "parrot":
        return [(188, 108), (324, 108), (360, 168), (340, 220), (292, 268), (256, 284), (220, 268), (172, 220), (152, 168)]
    if kind == "marlin":
        return [(200, 96), (312, 96), (348, 160), (328, 212), (288, 252), (256, 264), (224, 252), (184, 212), (164, 160)]
    if kind == "angel":
        return [(204, 132), (308, 132), (336, 180), (316, 220), (256, 240), (196, 220), (176, 180)]
    if kind == "lion":
        return [(200, 120), (312, 120), (340, 176), (320, 220), (256, 244), (192, 220), (172, 176)]
    if kind == "moray":
        return [(176, 100), (336, 100), (372, 168), (348, 220), (300, 268), (256, 292), (212, 268), (164, 220), (140, 168)]
    if kind == "trigger":
        return [(176, 96), (336, 96), (372, 164), (348, 216), (300, 256), (256, 268), (212, 256), (164, 216), (140, 164)]
    if kind == "seahorse":
        return [(208, 88), (304, 88), (332, 148), (316, 196), (280, 236), (256, 248), (232, 236), (196, 196), (180, 148)]
    return [(212, 128), (300, 128), (332, 176), (312, 216), (256, 232), (200, 216), (180, 176)]


def necks_of(kind: str) -> list[list[tuple[float, float]]]:
    if kind == "seahorse":
        return [[(240, 244), (272, 244), (280, 320), (256, 348), (232, 320)]]
    if kind == "moray":
        return [[(228, 276), (284, 276), (300, 348), (256, 388), (212, 348)]]
    if kind == "parrot":
        return [[(228, 268), (284, 268), (296, 332), (256, 360), (216, 332)]]
    return []


def inner_facets(face: list[tuple[float, float]]) -> list[list[tuple[float, float]]]:
    mx = sum(p[0] for p in face) / len(face)
    my = sum(p[1] for p in face) / len(face)
    mid = (mx, my)
    return [[point, face[(i + 1) % len(face)], mid] for i, point in enumerate(face)]


def tagged(
    items: list[tuple[list[tuple[float, float]], int, bool]], role: str
) -> list[tuple[list[tuple[float, float]], int, bool, str]]:
    return [(poly, alpha, rim, role) for poly, alpha, rim in items]


def body_of(kind: str) -> list[tuple[list[tuple[float, float]], int, bool, str]]:
    if kind == "parrot":
        torso = [(176, 248), (336, 248), (380, 340), (348, 448), (256, 500), (164, 448), (132, 340)]
        belly = [(216, 320), (296, 320), (312, 412), (256, 456), (200, 412)]
        return [(torso, 226, True, "body"), (belly, 200, True, "belly")]
    if kind == "marlin":
        torso = [(200, 236), (312, 236), (348, 320), (320, 420), (256, 468), (192, 420), (164, 320)]
        return [(torso, 228, True, "body")]
    if kind == "angel":
        disc = [(256, 40), (420, 140), (500, 256), (420, 400), (256, 508), (92, 400), (12, 256), (92, 140)]
        return [(disc, 200, True, "body")]
    if kind == "lion":
        torso = [(196, 228), (316, 228), (352, 320), (316, 420), (256, 460), (196, 420), (160, 320)]
        return [(torso, 222, True, "body")]
    if kind == "moray":
        tube = [(220, 280), (292, 288), (328, 360), (280, 428), (200, 400), (196, 332)]
        coil = [(160, 392), (352, 400), (420, 468), (352, 512), (160, 512), (92, 456)]
        return [(tube, 230, True, "body"), (coil, 220, True, "body")]
    if kind == "trigger":
        box = [(168, 220), (344, 220), (388, 320), (340, 440), (256, 488), (172, 440), (124, 320)]
        return [(box, 226, True, "body")]
    if kind == "seahorse":
        belly = [(216, 300), (296, 300), (320, 400), (256, 448), (192, 400)]
        return [(belly, 224, True, "belly")]
    wings = [(256, 200), (40, 120), (0, 220), (20, 340), (160, 400), (256, 280)]
    belly = [(196, 220), (316, 220), (340, 300), (256, 360), (172, 300)]
    return tagged(pair(wings, 210), "body") + [(belly, 200, True, "belly")]


def fish_parts(kind: str) -> list[tuple[list[tuple[float, float]], int, bool, str]]:
    if kind == "parrot":
        beak = [(220, 260), (292, 260), (276, 332), (256, 372), (236, 332)]
        gill = [(152, 168), (88, 188), (96, 248), (176, 220)]
        fin = [(132, 300), (8, 268), (0, 340), (40, 400), (164, 368)]
        dorsal = [(220, 108), (256, 8), (292, 108), (276, 128), (236, 128)]
        return (
            [(beak, 236, True, "beak"), (dorsal, 210, True, "fin")]
            + tagged(pair(gill, 216), "fin")
            + tagged(pair(fin, 214), "fin")
        )
    if kind == "marlin":
        bill = [(236, 252), (276, 252), (268, 380), (256, 468), (244, 380)]
        sail = [(200, 96), (168, 8), (256, 0), (344, 8), (312, 96), (292, 120), (220, 120)]
        pec = [(164, 212), (40, 188), (16, 248), (80, 280), (184, 236)]
        stripe = [(196, 260), (316, 260), (328, 284), (184, 284)]
        return (
            [(bill, 236, True, "bill"), (sail, 222, True, "sail"), (stripe, 190, False, "sail")]
            + tagged(pair(pec, 214), "accent")
        )
    if kind == "angel":
        streamer = [(308, 132), (460, 40), (500, 88), (420, 140), (336, 180)]
        crown = [(216, 88), (296, 88), (312, 132), (200, 132)]
        pec = [(176, 180), (48, 160), (28, 220), (96, 248), (196, 220)]
        return [(crown, 226, True, "crown")] + tagged(pair(streamer, 200), "accent") + tagged(pair(pec, 210), "accent")
    if kind == "lion":
        fan_a = [(172, 176), (20, 40), (0, 100), (36, 188), (160, 200)]
        fan_b = [(160, 220), (0, 220), (0, 300), (48, 348), (180, 252)]
        fan_c = [(196, 420), (48, 380), (8, 448), (64, 508), (200, 460)]
        bar = [(28, 80), (8, 96), (24, 140), (44, 120)]
        return tagged(pair(fan_a, 200), "fin") + tagged(pair(fan_b, 196), "fin") + tagged(pair(fan_c, 192), "fin") + tagged(pair(bar, 180, False), "stripe")
    if kind == "moray":
        jaw = [(176, 220), (80, 248), (72, 308), (196, 268)]
        grin = [(200, 268), (312, 268), (300, 300), (212, 300)]
        dorsal = [(176, 100), (120, 40), (256, 8), (392, 40), (336, 100), (300, 120), (212, 120)]
        return [(grin, 210, False, "accent"), (dorsal, 214, True, "accent")] + tagged(pair(jaw, 220), "body")
    if kind == "trigger":
        trigger = [(244, 20), (268, 20), (276, 96), (236, 96)]
        bar_a = [(176, 148), (336, 148), (348, 176), (164, 176)]
        bar_b = [(168, 300), (344, 300), (360, 336), (152, 336)]
        pec = [(140, 216), (24, 196), (8, 256), (72, 292), (164, 248)]
        mouth = [(232, 248), (280, 248), (268, 292), (256, 308), (244, 292)]
        return (
            [(trigger, 230, True, "spine"), (bar_a, 200, False, "stripe"), (bar_b, 196, False, "stripe"), (mouth, 220, True, "beak")]
            + tagged(pair(pec, 214), "accent")
        )
    if kind == "seahorse":
        snout = [(232, 232), (280, 232), (268, 320), (256, 368), (244, 320)]
        coronet = [(216, 40), (296, 40), (312, 88), (200, 88)]
        spike = [(244, 8), (268, 8), (272, 44), (240, 44)]
        plate = [(220, 348), (292, 348), (304, 396), (256, 424), (208, 396)]
        tail = [(208, 420), (304, 428), (360, 488), (300, 512), (196, 500), (152, 456)]
        fin = [(296, 300), (400, 268), (420, 332), (340, 360), (300, 336)]
        return [
            (snout, 234, True, "beak"),
            (coronet, 222, True, "crown"),
            (spike, 216, True, "spine"),
            (plate, 214, True, "belly"),
            (tail, 220, True, "body"),
            (fin, 200, True, "fin"),
        ]
    horn = [(180, 176), (80, 88), (40, 148), (132, 200), (200, 216)]
    tip = [(40, 120), (0, 80), (0, 160), (48, 176)]
    return tagged(pair(horn, 222), "horn") + tagged(pair(tip, 210), "accent")


def sheen_mask() -> np.ndarray:
    acc = np.zeros((SIZE, SIZE), dtype=np.uint8)
    for poly in (SHEEN_FACE, SHEEN_THROAT):
        acc = np.maximum(acc, poly_mask(poly))
    return acc


def paint_cast(kind: str, frame: int) -> Image.Image:
    arr = np.zeros((SIZE, SIZE, 4), dtype=np.uint8)
    light = light_vec(frame)
    index = 0
    for poly, alpha, rim, role in body_of(kind):
        pour_glass(arr, poly_mask(poly), glass_color(kind, role, index, frame), light, frame, alpha=alpha, rim=rim)
        index += 1
    for poly in necks_of(kind):
        pour_glass(arr, poly_mask(poly), glass_color(kind, "neck", index, frame), light, frame, alpha=228, rim=True)
        index += 1
    face = face_of(kind)
    pour_glass(arr, poly_mask(face), glass_color(kind, "face", index, frame), light, frame, alpha=236, rim=True)
    index += 1
    for poly in inner_facets(face):
        pour_glass(
            arr,
            poly_mask(poly),
            glass_color(kind, "facet", index, frame),
            light,
            frame,
            alpha=48,
            caustic_gain=0.08,
        )
        index += 1
    for poly, alpha, rim, role in fish_parts(kind):
        pour_glass(arr, poly_mask(poly), glass_color(kind, role, index, frame), light, frame, alpha=alpha, rim=rim)
        index += 1
    return Image.fromarray(arr, "RGBA")


def paint_sheen(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    arr = np.zeros((SIZE, SIZE, 4), dtype=np.uint8)
    mask = sheen_mask()
    ys, xs = np.nonzero(mask > 20)
    if xs.size == 0:
        return blank()
    t = clock(frame)
    base = SHEEN_HUE[kind]
    h = base + (xs.astype(np.float32) * 0.18 + ys.astype(np.float32) * 0.11) + math.degrees(t) * 0.55
    if kind == "prism":
        sat, val, a0 = 0.55, 0.90, 54.0
    elif kind == "quicksilver":
        sat, val, a0 = 0.16, 0.94, 46.0
    elif kind == "oil":
        sat, val, a0 = 0.50, 0.86, 48.0
    else:
        sat, val, a0 = 0.42, 0.84, 42.0
    rgb = hue_rgb(h, sat, val) * 255.0
    coverage = mask[ys, xs].astype(np.float32) / 255.0
    wave = 0.55 + 0.45 * np.sin(xs * 0.04 + ys * 0.03 + t * 1.4)
    alpha = np.clip(a0 * coverage * wave, 0, 160)
    add = np.zeros((SIZE, SIZE, 4), dtype=np.uint8)
    add[ys, xs, 0] = np.clip(rgb[:, 0], 0, 255).astype(np.uint8)
    add[ys, xs, 1] = np.clip(rgb[:, 1], 0, 255).astype(np.uint8)
    add[ys, xs, 2] = np.clip(rgb[:, 2], 0, 255).astype(np.uint8)
    add[ys, xs, 3] = alpha.astype(np.uint8)
    arr = composite_arr(arr, add)
    return Image.fromarray(arr, "RGBA")


def paint_regard(kind: str, frame: int) -> Image.Image:
    img = blank()
    draw = ImageDraw.Draw(img)
    t = clock(frame)
    blink = 0.22 if frame in (8, 9) else 1.0
    dim = 0.72 + 0.28 * math.sin(t)
    lx, ly = EYE_L
    rx, ry = EYE_R

    def inclusion(x: float, y: float, rx_: float, ry_: float, fill: tuple[int, int, int, int], highlight: bool = True) -> None:
        draw.ellipse((x - rx_, y - ry_, x + rx_, y + ry_), fill=fill)
        if highlight and blink > 0.5:
            draw.ellipse((x - rx_ * 0.28, y - ry_ * 0.55, x + rx_ * 0.05, y - ry_ * 0.12), fill=(236, 240, 244, 170))

    if kind == "quiet":
        a = int(220 * blink * dim)
        inclusion(lx, ly, 12, 15, (16, 14, 18, a))
        inclusion(rx, ry, 12, 15, (16, 14, 18, a))
    elif kind == "bloom":
        a = int(220 * blink)
        inclusion(lx, ly, 16, 18, (38, 26, 46, a))
        inclusion(rx, ry, 16, 18, (38, 26, 46, a))
        glow = int(90 + 50 * math.sin(t))
        draw.ellipse((lx - 7, ly - 7, lx + 7, ly + 7), fill=(220, 190, 255, glow))
        draw.ellipse((rx - 7, ry - 7, rx + 7, ry + 7), fill=(220, 190, 255, glow))
    elif kind == "slit":
        a = int(230 * blink)
        inclusion(lx, ly, 16, 5, (12, 12, 14, a), highlight=False)
        inclusion(rx, ry, 16, 5, (12, 12, 14, a), highlight=False)
        draw.ellipse((lx - 4, ly - 2, lx + 4, ly + 2), fill=(210, 220, 230, int(150 * blink)))
        draw.ellipse((rx - 4, ry - 2, rx + 4, ry + 2), fill=(210, 220, 230, int(150 * blink)))
    elif kind == "twin":
        a = int(200 * blink)
        for dx in (-8, 8):
            inclusion(lx + dx, ly, 7, 10, (20, 18, 26, a))
            inclusion(rx + dx, ry, 7, 10, (20, 18, 26, a))
    elif kind == "void":
        a = int(235 * blink)
        inclusion(lx, ly, 14, 16, (6, 6, 8, a), highlight=False)
        inclusion(rx, ry, 14, 16, (6, 6, 8, a), highlight=False)
    else:  # gleam
        pulse = int(160 + 70 * math.sin(t))
        inclusion(lx, ly, 11, 13, (18, 22, 26, int(220 * blink)))
        inclusion(rx, ry, 11, 13, (18, 22, 26, int(220 * blink)))
        draw.ellipse((lx - 5, ly - 5, lx + 5, ly + 5), fill=(210, 236, 240, pulse))
        draw.ellipse((rx - 5, ry - 5, rx + 5, ry + 5), fill=(210, 236, 240, pulse))
    return img


def metal_stroke(
    draw: ImageDraw.ImageDraw,
    pts: list[tuple[float, float]],
    width: int,
    fill: tuple[int, int, int, int],
    hi: tuple[int, int, int, int],
) -> None:
    draw.line(pts, fill=fill, width=width, joint="curve")
    draw.line([(p[0] - 1, p[1] - 1) for p in pts], fill=hi, width=max(1, width // 3), joint="curve")


def paint_crest(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    img = blank()
    draw = ImageDraw.Draw(img)
    t = clock(frame)
    glint = int(140 + 90 * max(0.0, math.sin(t)))
    plat = (188, 192, 198, 230)
    hi = (236, 238, 242, glint)
    gold = (198, 168, 104, 230)
    gold_hi = (240, 220, 160, glint)

    if kind == "band":
        metal_stroke(draw, [(196, 132), (256, 124), (316, 132)], 7, plat, hi)
        metal_stroke(draw, [(200, 138), (256, 130), (312, 138)], 3, (120, 124, 130, 160), (220, 224, 228, 90))
    elif kind == "shard":
        ox = math.sin(t) * 1.2
        shard = [(256 + ox, 48), (276 + ox, 108), (256 + ox, 98), (238 + ox, 108)]
        draw.polygon(shard, fill=(186, 210, 220, 150))
        draw.line([(256 + ox, 48), (276 + ox, 108)], fill=hi, width=2)
        draw.line([(256 + ox, 48), (238 + ox, 108)], fill=(80, 96, 110, 140), width=2)
    elif kind == "arc":
        box = (188, 58, 324, 168)
        draw.arc(box, 200, 340, fill=gold, width=5)
        draw.arc((190, 60, 322, 166), 205, 330, fill=gold_hi, width=2)
    elif kind == "spine":
        fin = [(252, 52), (262, 52), (268, 118), (246, 118)]
        draw.polygon(fin, fill=(176, 188, 198, 170))
        draw.line([(257, 52), (257, 118)], fill=hi, width=2)
    else:  # diadem
        metal_stroke(draw, [(190, 128), (256, 118), (322, 128)], 5, gold, gold_hi)
        for x in (216, 256, 296):
            draw.polygon([(x, 96), (x + 7, 118), (x - 7, 118)], fill=(220, 196, 140, 200))
            draw.ellipse((x - 3, 90, x + 3, 96), fill=(240, 228, 180, glint))
    return img


def paint_clasp(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    img = blank()
    draw = ImageDraw.Draw(img)
    t = clock(frame)
    glint = int(130 + 80 * max(0.0, math.cos(t)))
    plat = (176, 180, 186, 230)
    hi = (230, 234, 238, glint)
    gold = (186, 158, 96, 230)

    if kind == "bar":
        metal_stroke(draw, [(214, 332), (298, 332)], 8, plat, hi)
        draw.ellipse((208, 326, 220, 338), fill=plat)
        draw.ellipse((292, 326, 304, 338), fill=plat)
    elif kind == "drop":
        metal_stroke(draw, [(256, 318), (256, 348)], 3, plat, hi)
        draw.ellipse((246, 348, 266, 372), fill=(120, 160, 170, 150))
        draw.ellipse((250, 352, 260, 362), fill=(220, 236, 240, glint))
    elif kind == "torque":
        draw.arc((214, 300, 298, 372), 200, 340, fill=gold, width=7)
        draw.arc((218, 304, 294, 368), 210, 330, fill=(240, 220, 160, glint), width=2)
    elif kind == "pin":
        draw.polygon([(108, 388), (148, 378), (156, 392), (118, 404)], fill=plat)
        draw.ellipse((126, 382, 140, 396), fill=(90, 140, 150, 180))
        draw.ellipse((130, 385, 136, 391), fill=hi)
    else:  # coil
        for i, y in enumerate((324, 336, 348)):
            wobble = math.sin(t + i) * 2
            metal_stroke(draw, [(228 + wobble, y), (284 - wobble, y)], 4, plat, hi)
    return img


def wash_atelier(kind: str, frame: int) -> np.ndarray:
    top, mid, floor = ATELIER_WASH[kind]
    y = np.linspace(0.0, 1.0, SIZE, dtype=np.float32)[:, None]
    x = np.linspace(0.0, 1.0, SIZE, dtype=np.float32)[None, :]
    t = clock(frame)
    spot_x = 0.50 + 0.10 * math.cos(t)
    spot_y = 0.28 + 0.04 * math.sin(t * 0.7)
    wall = 1.0 - np.clip((y - 0.62) / 0.12, 0.0, 1.0)
    floor_w = 1.0 - wall
    c0 = np.array(top, dtype=np.float32)
    c1 = np.array(mid, dtype=np.float32)
    c2 = np.array(floor, dtype=np.float32)
    rgb = (c0 * (1.0 - y) + c1 * y) * wall + c2 * floor_w
    spot = np.exp(-(((x - spot_x) ** 2) / 0.11 + ((y - spot_y) ** 2) / 0.18))
    rgb = rgb + (36.0, 34.0, 40.0) * spot[..., None]
    gleam = 0.08 + 0.05 * math.sin(t)
    band = np.exp(-((y - 0.78) ** 2) / 0.004) * (0.55 + 0.45 * np.sin(x * 18 + t))
    rgb = rgb + gleam * 80.0 * band[..., None]
    rgb = np.clip(rgb, 0, 255)
    alpha = np.full((SIZE, SIZE, 1), 255.0, dtype=np.float32)
    return np.concatenate([rgb, alpha], axis=-1).astype(np.uint8)


def paint_atelier(kind: str, frame: int) -> Image.Image:
    arr = wash_atelier(kind, frame)
    img = Image.fromarray(arr, "RGBA")
    haze = img.filter(ImageFilter.GaussianBlur(radius=0.8))
    return Image.blend(img, haze, 0.18)


def paint_vapor(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    nx = (xx - 256.0) / 256.0
    ny = (yy - 256.0) / 256.0
    t = clock(frame)
    add = np.zeros((SIZE, SIZE, 4), dtype=np.uint8)
    if kind == "mist":
        drift = 0.05 * math.sin(t)
        band = np.exp(-((ny + 0.02 - drift) ** 2) / 0.045) * (0.55 + 0.22 * np.sin(xx * 0.014 + t))
        band += 0.42 * np.exp(-((ny + 0.36) ** 2) / 0.07)
        band += 0.28 * np.exp(-((ny - 0.24) ** 2) / 0.055)
        alpha = np.clip(band * 44.0, 0, 76)
        rgb = (214, 218, 224)
    elif kind == "mote":
        alpha = np.zeros((SIZE, SIZE), dtype=np.float32)
        for i in range(20):
            px = 256.0 + 190.0 * math.sin(t + i * 1.7) + 36.0 * math.cos(i * 1.3)
            py = 190.0 + 170.0 * math.cos(t * 0.75 + i * 2.05)
            radius = 10.0 + 4.0 * (i % 4)
            alpha += np.exp(-(((xx - px) ** 2 + (yy - py) ** 2) / (radius * radius)))
        alpha = np.clip(alpha * 88.0, 0, 78)
        rgb = (228, 232, 238)
    elif kind == "ribbon":
        path = ny - 0.32 * np.sin(nx * 2.1 + t) + 0.07 * math.sin(t * 1.2)
        alpha = np.clip(np.exp(-(path ** 2) / 0.011) * 52.0, 0, 76)
        rgb = (176, 208, 218)
    elif kind == "disc":
        d = nx ** 2 + (ny + 0.10) ** 2
        glow = np.exp(-d / 0.24) * (26.0 + 8.0 * math.sin(t))
        rim = np.exp(-((np.sqrt(np.maximum(d, 1e-6)) - 0.64) ** 2) / 0.005) * 44.0
        alpha = np.clip(glow + rim, 0, 82)
        rgb = (224, 218, 208)
    elif kind == "plume":
        sway = 0.09 * math.sin(t)
        d = ((nx - sway) ** 2) / 0.055 + ((ny - 0.72) ** 2) / 0.40
        alpha = np.clip(np.exp(-d) * (48.0 + 10.0 * math.sin(t)), 0, 78)
        rgb = (204, 210, 218)
    else:
        pool = ((nx ** 2) / 0.20) + (((ny - 0.64) ** 2) / 0.09)
        glow = np.exp(-pool) * (38.0 + 10.0 * math.sin(t))
        rise = np.exp(-((nx ** 2) / 0.07 + ((ny - 0.18) ** 2) / 0.50)) * 14.0
        alpha = np.clip(glow + rise, 0, 80)
        rgb = (168, 196, 204)
    add[..., 0] = rgb[0]
    add[..., 1] = rgb[1]
    add[..., 2] = rgb[2]
    add[..., 3] = alpha.astype(np.uint8)
    return Image.fromarray(add, "RGBA")


TRAIT_SPEC: dict[str, list[tuple[str, str, int]]] = {
    "atelier": [
        ("obsidian", "Obsidian Room", 16),
        ("slate", "Slate Studio", 16),
        ("dusk", "Dusk Chamber", 14),
        ("ivory", "Ivory Gallery", 14),
        ("mercury", "Mercury Wall", 12),
        ("wine", "Wine Vault", 10),
        ("brine", "Brine Hall", 10),
        ("quartz", "Quartz Court", 8),
    ],
    "vapor": [
        ("none", "Clear Air", 22),
        ("mist", "Soft Mist", 18),
        ("mote", "Glass Motes", 16),
        ("ribbon", "Caustic Ribbon", 14),
        ("disc", "Pale Disc", 12),
        ("plume", "Rising Plume", 10),
        ("well", "Luminous Well", 8),
    ],
    "cast": [
        ("parrot", "Parrotfish", 18),
        ("marlin", "Blue Marlin", 16),
        ("angel", "Queen Angel", 14),
        ("lion", "Lionfish", 14),
        ("trigger", "Triggerfish", 12),
        ("seahorse", "Seahorse", 10),
        ("moray", "Green Moray", 8),
        ("manta", "Manta", 8),
    ],
    "sheen": [
        ("none", "Bare Glass", 22),
        ("oil", "Oil Film", 18),
        ("aurora", "Aurora Film", 16),
        ("rose", "Rose Film", 14),
        ("peacock", "Peacock Film", 12),
        ("quicksilver", "Quicksilver Film", 10),
        ("prism", "Prism Film", 8),
    ],
    "regard": [
        ("quiet", "Quiet", 24),
        ("bloom", "Bloom", 18),
        ("slit", "Slit", 16),
        ("twin", "Twin", 14),
        ("void", "Void", 14),
        ("gleam", "Gleam", 14),
    ],
    "crest": [
        ("none", "Bare Crown", 28),
        ("band", "Platinum Band", 18),
        ("shard", "Prism Shard", 16),
        ("arc", "Gold Arc", 14),
        ("spine", "Glass Spine", 12),
        ("diadem", "Thin Diadem", 12),
    ],
    "clasp": [
        ("none", "Bare Neck", 28),
        ("bar", "Bar Clasp", 18),
        ("drop", "Glass Drop", 16),
        ("torque", "Gold Torque", 14),
        ("pin", "Shoulder Pin", 12),
        ("coil", "Coil", 12),
    ],
}

PAINTERS = {
    "atelier": {k: (lambda kind: (lambda frame, k=kind: paint_atelier(k, frame)))(k) for k in ATELIERS},
    "vapor": {k: (lambda kind: (lambda frame, k=kind: paint_vapor(k, frame)))(k) for k in VAPORS},
    "cast": {k: (lambda kind: (lambda frame, k=kind: paint_cast(k, frame)))(k) for k in CASTS},
    "sheen": {k: (lambda kind: (lambda frame, k=kind: paint_sheen(k, frame)))(k) for k in SHEENS},
    "regard": {k: (lambda kind: (lambda frame, k=kind: paint_regard(k, frame)))(k) for k in REGARDS},
    "crest": {k: (lambda kind: (lambda frame, k=kind: paint_crest(k, frame)))(k) for k in CRESTS},
    "clasp": {k: (lambda kind: (lambda frame, k=kind: paint_clasp(k, frame)))(k) for k in CLASPS},
}

STACK = ("atelier", "vapor", "cast", "sheen", "regard", "crest", "clasp")

SIGNATURES = [
    {"atelier": "dusk", "vapor": "disc", "cast": "parrot", "sheen": "oil", "regard": "quiet", "crest": "band", "clasp": "drop"},
    {"atelier": "obsidian", "vapor": "well", "cast": "manta", "sheen": "quicksilver", "regard": "void", "crest": "spine", "clasp": "bar"},
    {"atelier": "ivory", "vapor": "mist", "cast": "parrot", "sheen": "rose", "regard": "bloom", "crest": "diadem", "clasp": "torque"},
    {"atelier": "brine", "vapor": "plume", "cast": "seahorse", "sheen": "peacock", "regard": "gleam", "crest": "shard", "clasp": "none"},
    {"atelier": "wine", "vapor": "ribbon", "cast": "lion", "sheen": "prism", "regard": "slit", "crest": "arc", "clasp": "pin"},
    {"atelier": "mercury", "vapor": "mote", "cast": "angel", "sheen": "aurora", "regard": "twin", "crest": "band", "clasp": "coil"},
    {"atelier": "slate", "vapor": "none", "cast": "marlin", "sheen": "none", "regard": "quiet", "crest": "none", "clasp": "bar"},
    {"atelier": "quartz", "vapor": "disc", "cast": "trigger", "sheen": "oil", "regard": "bloom", "crest": "diadem", "clasp": "drop"},
    {"atelier": "dusk", "vapor": "mist", "cast": "moray", "sheen": "quicksilver", "regard": "gleam", "crest": "shard", "clasp": "torque"},
    {"atelier": "obsidian", "vapor": "plume", "cast": "seahorse", "sheen": "rose", "regard": "void", "crest": "arc", "clasp": "none"},
    {"atelier": "ivory", "vapor": "mote", "cast": "angel", "sheen": "prism", "regard": "slit", "crest": "spine", "clasp": "pin"},
    {"atelier": "brine", "vapor": "well", "cast": "manta", "sheen": "aurora", "regard": "twin", "crest": "band", "clasp": "coil"},
    {"atelier": "wine", "vapor": "ribbon", "cast": "marlin", "sheen": "peacock", "regard": "quiet", "crest": "none", "clasp": "drop"},
    {"atelier": "mercury", "vapor": "disc", "cast": "lion", "sheen": "oil", "regard": "bloom", "crest": "diadem", "clasp": "bar"},
    {"atelier": "slate", "vapor": "none", "cast": "trigger", "sheen": "none", "regard": "gleam", "crest": "shard", "clasp": "torque"},
    {"atelier": "quartz", "vapor": "mist", "cast": "moray", "sheen": "rose", "regard": "void", "crest": "arc", "clasp": "pin"},
]

TRAIT_LABELS = (
    ("atelier", "Atelier"),
    ("vapor", "Vapor"),
    ("cast", "Cast"),
    ("sheen", "Sheen"),
    ("regard", "Regard"),
    ("crest", "Crest"),
    ("clasp", "Clasp"),
)

COLLECTION_DESCRIPTION = (
    "Opaline is a 5,555-piece collection of looping smoked-glass PFP GIFs. "
    "Each portrait is stacked from seven layers — atelier, vapor, cast, sheen, regard, crest, and clasp — "
    "then flattened onto one 12-frame GIF. Eight crystal reef fish. Dichroic film. Editorial light."
)

COLLECTION_STORY = (
    "Opaline.\n\n"
    "A 5,555-piece collection of looping smoked-glass PFP GIFs on Base. "
    "Each portrait is stacked from seven layers — atelier, vapor, cast, sheen, regard, crest, and clasp — "
    "then flattened onto one 12-frame GIF. Eight saltwater fish, each its own glass: parrotfish, "
    "blue marlin, queen angelfish, lionfish, triggerfish, seahorse, green moray, and manta. "
    "Vapor hangs in the room. Light walks the facets. Film shifts hue. Inclusions dim.\n\n"
    "Crystal reef fish. Seven films, including bare glass. No charcoal outline. No sticker cutout. "
    "The fish stays seated. One shared clock.\n\n"
    "Minting on Base (chain ID 8453). Gas is ETH."
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
        "name": "Opaline",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Eight glass reef fish share one eye line; crests and clasps never edit the cast.",
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
                "name": f"Opaline #{index}",
                "image": f"/opaline-preview/{index}.gif",
                "attributes": [
                    {"trait_type": label, "value": name_of(key, selection[key])} for key, label in TRAIT_LABELS
                ],
            }
        )
    (PREVIEW_DIR / "samples.json").write_text(json.dumps(samples, indent=2) + "\n", encoding="utf-8")
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
            f'    image: "{sample["image"]}?v=6",\n'
            f"    attributes: [\n      {attrs},\n    ],\n"
            "  }"
        )
    (SRC_DATA / "opaline-gallery.ts").write_text(
        "export type OpalineSample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const opalineSamples: OpalineSample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array(
        [
            [0.06, 0.06, 0.08],
            [0.18, 0.16, 0.22],
            [0.42, 0.36, 0.32],
            [0.12, 0.14, 0.18],
        ],
        dtype=np.float32,
    )
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)
    y = np.linspace(0.0, 1.0, height, dtype=np.float32)
    xx, yy = np.meshgrid(x, y)
    t = np.clip(xx * 0.55 + yy * 0.45, 0.0, 0.999) * (len(colors) - 1)
    i0 = np.floor(t).astype(np.int32)
    f = (t - i0)[..., None]
    c0 = colors[i0]
    c1 = colors[np.clip(i0 + 1, 0, len(colors) - 1)]
    rgb_out = c0 * (1.0 - f) + c1 * f
    arr = np.dstack([np.clip(rgb_out * 255.0, 0, 255).astype(np.uint8), np.full((height, width), 255, dtype=np.uint8)])
    return Image.fromarray(arr, "RGBA")


def write_collection_meta() -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    (META_DIR / "opaline-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "opaline.json").write_text(
        json.dumps(
            {
                "name": "Opaline",
                "symbol": "OPAL",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-opaline.gif",
                "featured_image": "/brand/featured-opaline.jpg",
                "banner_image": "/brand/banner-opaline.png",
                "opensea_banner_image": "/brand/banner-opaline-opensea.jpg",
                "external_link": "/opaline",
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
    ImageDraw.Draw(mask).rounded_rectangle((16, 16, SIZE - 17, SIZE - 17), radius=48, fill=255)
    logo.putalpha(Image.composite(logo.split()[-1], Image.new("L", (SIZE, SIZE), 0), mask))
    rim = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(rim).rounded_rectangle((12, 12, SIZE - 13, SIZE - 13), radius=52, outline=(198, 202, 208, 255), width=4)
    logo = Image.alpha_composite(logo, rim)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-opaline.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-opaline-loop.png",
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
            place_portrait(canvas, portrait, px, y, size, radius=max(28, size // 12))
        return canvas

    save_image(lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-opaline.png", quality=94)
    save_image(lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-opaline-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=48)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=48)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-opaline.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(
        gif_frames,
        BRAND_DIR / "collection-opaline.gif",
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
        print("Writing Opaline brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Opaline smoked-glass reef fish…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
