#!/usr/bin/env python3
"""Paint Opaline — smoked-glass beasts with iridescent film.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
The beast is seated: no bounce, no hover. Light walks the facets.
Vapor hangs in the room. Sheen hue-shifts. Regard inclusions dim.

Look: eight crystal creatures — stag, serpent, moth, beetle, ram, ibis,
wyrm, mantis. Angular glass, not charcoal, not stickers, not an egg body.
Dichroic film. Platinum jewelry. Editorial studio rooms.
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
CASTS = ("stag", "serpent", "moth", "beetle", "ram", "ibis", "wyrm", "mantis")
SHEENS = ("none", "oil", "aurora", "rose", "peacock", "quicksilver", "prism")
REGARDS = ("quiet", "bloom", "slit", "twin", "void", "gleam")
CRESTS = ("none", "band", "shard", "arc", "spine", "diadem")
CLASPS = ("none", "bar", "drop", "torque", "pin", "coil")

CAST_RGB = {
    "stag": (198, 176, 148),
    "serpent": (58, 112, 92),
    "moth": (214, 218, 224),
    "beetle": (156, 92, 64),
    "ram": (118, 112, 118),
    "ibis": (62, 118, 126),
    "wyrm": (104, 72, 122),
    "mantis": (32, 34, 40),
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
# Nothing else is shared — each cast is its own animal skull and body.
EYE_L = (220.0, 184.0)
EYE_R = (292.0, 184.0)
SHEEN_FACE = [(214, 140), (298, 140), (316, 184), (300, 220), (256, 236), (212, 220), (196, 184)]
SHEEN_THROAT = [(242, 280), (270, 280), (276, 340), (236, 340)]


def mirror(poly: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(512.0 - x, y) for x, y in poly]


def pair(poly: list[tuple[float, float]], alpha: int, rim: bool = True) -> list[tuple[list[tuple[float, float]], int, bool]]:
    return [(poly, alpha, rim), (mirror(poly), alpha, rim)]


def face_of(kind: str) -> list[tuple[float, float]]:
    """Animal skulls. Wide enough to hold the shared eyes, never a mannequin hex."""
    if kind == "stag":
        return [
            (218, 76),
            (294, 76),
            (336, 140),
            (322, 196),
            (292, 268),
            (272, 348),
            (256, 388),
            (240, 348),
            (220, 268),
            (190, 196),
            (176, 140),
        ]
    if kind == "serpent":
        return [(256, 88), (352, 148), (340, 196), (300, 236), (256, 284), (212, 236), (172, 196), (160, 148)]
    if kind == "moth":
        return [(196, 148), (316, 148), (340, 184), (320, 216), (256, 232), (192, 216), (172, 184)]
    if kind == "beetle":
        return [(216, 88), (296, 88), (336, 156), (320, 204), (256, 236), (192, 204), (176, 156)]
    if kind == "ram":
        return [
            (156, 84),
            (356, 84),
            (384, 148),
            (356, 208),
            (320, 284),
            (288, 364),
            (256, 412),
            (224, 364),
            (192, 284),
            (156, 208),
            (128, 148),
        ]
    if kind == "ibis":
        return [(228, 124), (284, 124), (312, 168), (298, 200), (256, 216), (214, 200), (200, 168)]
    if kind == "wyrm":
        return [
            (200, 68),
            (312, 68),
            (360, 144),
            (344, 200),
            (308, 276),
            (280, 368),
            (256, 428),
            (232, 368),
            (204, 276),
            (168, 200),
            (152, 144),
        ]
    return [(256, 20), (400, 176), (348, 228), (256, 252), (164, 228), (112, 176)]


def necks_of(kind: str) -> list[list[tuple[float, float]]]:
    if kind == "ibis":
        return [[(246, 208), (278, 214), (304, 268), (336, 340), (308, 408), (260, 436), (244, 360), (256, 284)]]
    if kind == "moth":
        return [[(236, 228), (276, 228), (280, 272), (256, 292), (232, 272)]]
    if kind == "mantis":
        return [[(244, 248), (268, 248), (274, 308), (256, 328), (238, 308)]]
    if kind == "stag":
        return [[(236, 360), (276, 360), (292, 428), (256, 468), (220, 428)]]
    if kind == "ram":
        return [[(228, 388), (284, 388), (300, 456), (256, 492), (212, 456)]]
    return []


def inner_facets(face: list[tuple[float, float]]) -> list[list[tuple[float, float]]]:
    mx = sum(p[0] for p in face) / len(face)
    my = sum(p[1] for p in face) / len(face)
    mid = (mx, my)
    return [[point, face[(i + 1) % len(face)], mid] for i, point in enumerate(face)]


def body_of(kind: str) -> list[tuple[list[tuple[float, float]], int, bool]]:
    if kind == "serpent":
        hood = [
            (256, 8),
            (412, 48),
            (508, 132),
            (512, 220),
            (468, 292),
            (348, 248),
            (256, 204),
            (164, 248),
            (44, 292),
            (0, 220),
            (4, 132),
            (100, 48),
        ]
        tube = [(236, 260), (284, 268), (312, 332), (248, 388), (196, 348), (220, 300)]
        coil_a = [(148, 348), (364, 348), (424, 420), (364, 492), (148, 492), (88, 420)]
        coil_b = [(196, 412), (316, 412), (368, 468), (316, 512), (196, 512), (144, 468)]
        return [(hood, 204, True), (tube, 232, True), (coil_a, 226, True), (coil_b, 220, True)]
    if kind == "moth":
        upper = [(196, 152), (64, 0), (0, 72), (8, 176), (108, 228), (220, 188)]
        lower = [(200, 196), (8, 208), (0, 332), (48, 500), (196, 444), (232, 252)]
        scallop_a = [(72, 24), (16, 40), (8, 96), (68, 120), (116, 72)]
        scallop_b = [(40, 260), (0, 288), (12, 360), (72, 348), (96, 292)]
        return pair(upper, 190) + pair(lower, 196) + pair(scallop_a, 150, False) + pair(scallop_b, 146, False)
    if kind == "beetle":
        shell = [(200, 216), (72, 260), (36, 368), (80, 488), (256, 512), (256, 224)]
        split = [(246, 224), (266, 224), (266, 508), (246, 508)]
        leg_a = [(72, 260), (0, 216), (0, 252), (68, 284)]
        leg_b = [(52, 340), (0, 348), (4, 388), (72, 364)]
        leg_c = [(80, 428), (4, 468), (28, 504), (108, 452)]
        return pair(shell, 234) + [(split, 200, False)] + pair(leg_a, 210) + pair(leg_b, 210) + pair(leg_c, 210)
    if kind == "ibis":
        body = [(240, 392), (188, 424), (176, 484), (256, 512), (360, 476), (372, 416), (320, 384)]
        return [(body, 218, True)]
    if kind == "mantis":
        thorax = [(228, 248), (284, 248), (300, 308), (256, 336), (212, 308)]
        abdomen = [(236, 328), (276, 328), (296, 412), (256, 488), (216, 412)]
        return [(thorax, 226, True), (abdomen, 220, True)]
    return []


def beast_parts(kind: str) -> list[tuple[list[tuple[float, float]], int, bool]]:
    if kind == "stag":
        beam = [(218, 76), (160, 16), (64, 0), (40, 28), (120, 36), (204, 76)]
        tine_a = [(64, 0), (0, 12), (16, 48), (76, 28)]
        tine_b = [(160, 16), (96, 0), (108, 40)]
        tine_c = [(120, 36), (60, 56), (104, 84)]
        tine_d = [(40, 28), (8, 72), (52, 60)]
        ear = [(176, 140), (48, 64), (88, 188), (196, 188)]
        nostril = [(240, 352), (256, 384), (248, 356)]
        return (
            pair(beam, 232)
            + pair(tine_a, 224)
            + pair(tine_b, 216, False)
            + pair(tine_c, 214, False)
            + pair(tine_d, 210, False)
            + pair(ear, 230)
            + [(nostril, 200, False), (mirror(nostril), 200, False)]
        )
    if kind == "serpent":
        fang = [(220, 260), (256, 312), (244, 264)]
        tongue = [(248, 280), (256, 348), (264, 280)]
        fork_l = [(256, 348), (232, 380), (252, 352)]
        fork_r = [(256, 348), (280, 380), (260, 352)]
        return [(fang, 214, False), (mirror(fang), 214, False), (tongue, 200, False), (fork_l, 196, False), (fork_r, 196, False)]
    if kind == "moth":
        antenna = [(196, 148), (128, 40), (36, 0), (16, 28), (116, 64), (192, 144)]
        club = [(36, 0), (0, 8), (8, 36), (40, 20)]
        return pair(antenna, 216) + pair(club, 208)
    if kind == "beetle":
        horn = [(246, 0), (266, 0), (280, 100), (232, 100)]
        flare = [(256, 0), (340, 36), (256, 28), (172, 36)]
        mandible = [(192, 204), (96, 220), (88, 292), (204, 232)]
        return [(horn, 236, True), (flare, 220, True)] + pair(mandible, 228)
    if kind == "ram":
        brow = [(164, 84), (348, 84), (364, 136), (148, 136)]
        curl_a = [(156, 100), (64, 12), (0, 72), (8, 168), (88, 188), (156, 136)]
        curl_b = [(0, 72), (0, 188), (16, 292), (84, 268), (20, 176)]
        curl_c = [(16, 292), (48, 384), (140, 348), (88, 276), (84, 268)]
        nose = [(228, 360), (284, 360), (276, 404), (256, 420), (236, 404)]
        return [(brow, 228, True), (nose, 220, True)] + pair(curl_a, 234) + pair(curl_b, 226) + pair(curl_c, 218)
    if kind == "ibis":
        beak = [
            (214, 188),
            (298, 200),
            (280, 268),
            (220, 348),
            (140, 428),
            (64, 484),
            (16, 512),
            (4, 488),
            (64, 448),
            (140, 380),
            (200, 288),
        ]
        plume = [(256, 4), (360, 52), (376, 108), (312, 128), (200, 120), (140, 52)]
        return [(beak, 236, True), (plume, 222, True)]
    if kind == "wyrm":
        horn = [(200, 68), (248, 68), (200, 0), (128, 16)]
        brow = [(168, 144), (64, 72), (36, 164), (156, 176)]
        frill = [(152, 176), (24, 188), (8, 248), (148, 220)]
        jaw = [(168, 200), (72, 220), (48, 284), (160, 256)]
        fork = [(232, 368), (256, 440), (244, 376)]
        return (
            pair(horn, 230)
            + pair(brow, 222)
            + pair(frill, 208, False)
            + pair(jaw, 216)
            + [(fork, 210, False), (mirror(fork), 210, False)]
        )
    scythe = [(164, 228), (28, 88), (0, 136), (12, 216), (88, 224), (180, 248)]
    blade = [(0, 136), (0, 292), (20, 412), (88, 508), (60, 348), (12, 216)]
    tooth_a = [(20, 280), (0, 300), (28, 320)]
    tooth_b = [(28, 360), (8, 384), (40, 400)]
    return pair(scythe, 222) + pair(blade, 216) + pair(tooth_a, 200, False) + pair(tooth_b, 196, False)


def sheen_mask() -> np.ndarray:
    acc = np.zeros((SIZE, SIZE), dtype=np.uint8)
    for poly in (SHEEN_FACE, SHEEN_THROAT):
        acc = np.maximum(acc, poly_mask(poly))
    return acc


def paint_cast(kind: str, frame: int) -> Image.Image:
    arr = np.zeros((SIZE, SIZE, 4), dtype=np.uint8)
    light = light_vec(frame)
    rgb = CAST_RGB[kind]
    neck_rgb = tuple(max(0, c - 22) for c in rgb)
    for poly, alpha, rim in body_of(kind):
        pour_glass(arr, poly_mask(poly), rgb, light, frame, alpha=alpha, rim=rim)
    for poly in necks_of(kind):
        pour_glass(arr, poly_mask(poly), neck_rgb, light, frame, alpha=230, rim=True)
    face = face_of(kind)
    pour_glass(arr, poly_mask(face), rgb, light, frame, alpha=236, rim=True)
    tint = tuple(min(255, max(0, c + offset)) for c, offset in zip(rgb, (8, -4, 6)))
    for poly in inner_facets(face):
        pour_glass(arr, poly_mask(poly), tint, light, frame, alpha=40, caustic_gain=0.08)
    for poly, alpha, rim in beast_parts(kind):
        pour_glass(arr, poly_mask(poly), rgb, light, frame, alpha=alpha, rim=rim)
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
        ("stag", "Stag", 18),
        ("serpent", "Serpent", 16),
        ("moth", "Moth", 14),
        ("beetle", "Beetle", 14),
        ("ram", "Ram", 12),
        ("ibis", "Ibis", 10),
        ("wyrm", "Wyrm", 8),
        ("mantis", "Mantis", 8),
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
    {"atelier": "dusk", "vapor": "disc", "cast": "stag", "sheen": "oil", "regard": "quiet", "crest": "band", "clasp": "drop"},
    {"atelier": "obsidian", "vapor": "well", "cast": "mantis", "sheen": "quicksilver", "regard": "void", "crest": "spine", "clasp": "bar"},
    {"atelier": "ivory", "vapor": "mist", "cast": "stag", "sheen": "rose", "regard": "bloom", "crest": "diadem", "clasp": "torque"},
    {"atelier": "brine", "vapor": "plume", "cast": "ibis", "sheen": "peacock", "regard": "gleam", "crest": "shard", "clasp": "none"},
    {"atelier": "wine", "vapor": "ribbon", "cast": "wyrm", "sheen": "prism", "regard": "slit", "crest": "arc", "clasp": "pin"},
    {"atelier": "mercury", "vapor": "mote", "cast": "moth", "sheen": "aurora", "regard": "twin", "crest": "band", "clasp": "coil"},
    {"atelier": "slate", "vapor": "none", "cast": "serpent", "sheen": "none", "regard": "quiet", "crest": "none", "clasp": "bar"},
    {"atelier": "quartz", "vapor": "disc", "cast": "beetle", "sheen": "oil", "regard": "bloom", "crest": "diadem", "clasp": "drop"},
    {"atelier": "dusk", "vapor": "mist", "cast": "ram", "sheen": "quicksilver", "regard": "gleam", "crest": "shard", "clasp": "torque"},
    {"atelier": "obsidian", "vapor": "plume", "cast": "ibis", "sheen": "rose", "regard": "void", "crest": "arc", "clasp": "none"},
    {"atelier": "ivory", "vapor": "mote", "cast": "moth", "sheen": "prism", "regard": "slit", "crest": "spine", "clasp": "pin"},
    {"atelier": "brine", "vapor": "well", "cast": "mantis", "sheen": "aurora", "regard": "twin", "crest": "band", "clasp": "coil"},
    {"atelier": "wine", "vapor": "ribbon", "cast": "serpent", "sheen": "peacock", "regard": "quiet", "crest": "none", "clasp": "drop"},
    {"atelier": "mercury", "vapor": "disc", "cast": "wyrm", "sheen": "oil", "regard": "bloom", "crest": "diadem", "clasp": "bar"},
    {"atelier": "slate", "vapor": "none", "cast": "beetle", "sheen": "none", "regard": "gleam", "crest": "shard", "clasp": "torque"},
    {"atelier": "quartz", "vapor": "mist", "cast": "ram", "sheen": "rose", "regard": "void", "crest": "arc", "clasp": "pin"},
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
    "Opaline is a 10,000-piece collection of looping smoked-glass PFP GIFs. "
    "Each portrait is stacked from seven layers — atelier, vapor, cast, sheen, regard, crest, and clasp — "
    "then flattened onto one 12-frame GIF. Eight crystal beasts. Dichroic film. Editorial light."
)

COLLECTION_STORY = (
    "Opaline.\n\n"
    "A 10,000-piece collection of looping smoked-glass PFP GIFs on Base. "
    "Each portrait is stacked from seven layers — atelier, vapor, cast, sheen, regard, crest, and clasp — "
    "then flattened onto one 12-frame GIF. Eight beasts, each its own animal: stag, serpent, moth, "
    "beetle, ram, ibis, wyrm, and mantis. Vapor hangs in the room. Light walks the facets. "
    "Film shifts hue. Inclusions dim.\n\n"
    "Crystal creatures. Seven films, including bare glass. No charcoal outline. No sticker cutout. "
    "The beast stays seated. One shared clock.\n\n"
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
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Eight glass beasts share one eye line; crests and clasps never edit the cast.",
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
            f'    image: "{sample["image"]}?v=5",\n'
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
    print("Building Opaline smoked-glass beasts…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
