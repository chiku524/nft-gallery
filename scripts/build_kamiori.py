#!/usr/bin/env python3
"""Paint Kamiori — origami paper beings.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
The fold stays seated in one envelope. A draft lifts one corner.
Language: polygonal facets, valley/mountain scores, deckle washi.
Not intaglio hatch. Not risograph blots. Not charcoal. Not stickers.
Not a postage rectangle. Not a seated engraved bust.
"""

from __future__ import annotations

import argparse
import hashlib
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

TRAIT_DIR = ROOT / "public" / "kamiori-traits"
PREVIEW_DIR = ROOT / "public" / "kamiori-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

PULPS = ("cream", "indigo", "vermilion", "moss", "peach", "gold", "ink", "frost")
FLECKS = ("none", "kozo", "golddust", "speckle", "stripe", "cloud")
FOLDS = ("crane", "frog", "beetle", "boat", "hare", "fan", "kite", "lotus")
SCORES = ("none", "mountain", "valley", "diagram", "radial", "grid")
FACETS = ("none", "wing", "body", "tip", "band", "gore")
SEALS = ("none", "hanko", "twin", "loop", "tassel")
DRAFTS = ("none", "lift", "flutter", "scrap", "gust")

# Washi dyes. Not postage inks and not risograph fluorescents.
DYE = {
    "cream": (246, 240, 228),
    "indigo": (36, 52, 92),
    "vermilion": (196, 69, 45),
    "moss": (74, 98, 62),
    "peach": (232, 186, 156),
    "gold": (196, 156, 72),
    "ink": (28, 26, 24),
    "frost": (228, 232, 236),
}

FOLD_DYE = {
    "crane": "vermilion",
    "frog": "moss",
    "beetle": "indigo",
    "boat": "gold",
    "hare": "peach",
    "fan": "cream",
    "kite": "frost",
    "lotus": "vermilion",
}


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def clock(frame: int) -> float:
    return frame / FRAMES * math.tau


def seed_for(*parts: object) -> int:
    payload = "|".join(map(str, parts)).encode()
    return int(hashlib.md5(payload).hexdigest()[:8], 16)


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(round(x + (y - x) * t)) for x, y in zip(a, b))


def luma(rgb: tuple[int, int, int]) -> float:
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def contrast_on(paper: tuple[int, int, int], dye: tuple[int, int, int]) -> tuple[int, int, int]:
    if abs(luma(paper) - luma(dye)) < 48:
        return DYE["cream"] if luma(paper) < 128 else DYE["ink"]
    return dye


def shade(rgb: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(max(0, min(255, int(c * amount))) for c in rgb)


def lift_of(frame: int, kind: str) -> float:
    t = clock(frame)
    if kind == "none":
        return math.sin(t) * 1.2
    if kind == "lift":
        return math.sin(t) * 10.0
    if kind == "flutter":
        return math.sin(t * 2) * 7.0 + math.cos(t) * 3.0
    if kind == "scrap":
        return math.sin(t) * 5.0
    return math.sin(t) * 14.0 + math.cos(t * 1.3) * 4.0


def deckle_mask(frame: int) -> np.ndarray:
    rng = np.random.RandomState(seed_for("deckle"))
    margin = 30
    yy, xx = np.mgrid[0:SIZE, 0:SIZE]
    # Soft rectangle, then chew the edge with low-frequency noise — torn washi, not perfs.
    dist = np.minimum.reduce(
        [
            xx - margin,
            yy - margin,
            (SIZE - 1 - margin) - xx,
            (SIZE - 1 - margin) - yy,
        ]
    ).astype(np.float32)
    noise = rng.randn(SIZE, SIZE).astype(np.float32)
    noise = Image.fromarray(((noise + 3) * 40).clip(0, 255).astype(np.uint8), "L")
    noise = np.asarray(noise.filter(ImageFilter.GaussianBlur(radius=6)), dtype=np.float32)
    t = math.sin(clock(frame)) * 1.4
    edge = dist + (noise - 128.0) * 0.11 + t
    alpha = np.clip(edge * 18.0, 0, 255).astype(np.uint8)
    return alpha


def paint_pulp(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    base = np.array(DYE[kind], dtype=np.float32)
    rng = np.random.RandomState(seed_for("pulp", kind))
    laid = rng.randn(SIZE, SIZE).astype(np.float32) * 3.1
    # Chain lines of washi — parallel fiber, not hatch engraving.
    yy = np.arange(SIZE, dtype=np.float32)[:, None]
    xx = np.arange(SIZE, dtype=np.float32)[None, :]
    chain = np.sin((yy * 0.9 + xx * 0.08) * 0.35 + clock(frame) * 0.15) * 2.6
    rgb = np.clip(base + laid[..., None] + chain[..., None], 0, 255).astype(np.uint8)
    alpha = deckle_mask(frame)
    return Image.fromarray(np.dstack([rgb, alpha]), "RGBA")


def paint_fleck(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    layer = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(layer)
    rng = np.random.RandomState(seed_for("fleck", kind))
    t = clock(frame)
    if kind == "kozo":
        for _ in range(90):
            x = int(rng.randint(40, 472))
            y = int(rng.randint(40, 472))
            a = rng.random() * math.tau
            length = 8 + rng.random() * 18
            draw.line(
                [(x, y), (x + math.cos(a) * length, y + math.sin(a) * length * 0.4)],
                fill=int(90 + rng.random() * 80),
                width=1,
            )
    elif kind == "golddust":
        for _ in range(70):
            x = int((rng.random() * 420 + 46 + math.sin(t + rng.random()) * 2))
            y = int(rng.random() * 420 + 46)
            r = 1 + int(rng.random() * 2)
            draw.ellipse((x - r, y - r, x + r, y + r), fill=160)
    elif kind == "speckle":
        for _ in range(220):
            x, y = int(rng.randint(36, 476)), int(rng.randint(36, 476))
            draw.point((x, y), fill=140)
    elif kind == "stripe":
        for i in range(18):
            y = 48 + i * 24 + int(math.sin(t + i) * 1.5)
            draw.line([(40, y), (472, y + 6)], fill=70, width=1)
    else:  # cloud
        for i in range(6):
            cx = 90 + i * 62
            cy = 200 + int(math.sin(t * 0.6 + i) * 8)
            draw.ellipse((cx - 50, cy - 22, cx + 70, cy + 28), fill=55)
    window = deckle_mask(frame)
    mask = np.minimum(np.asarray(layer, dtype=np.uint8), window)
    rgb = DYE["ink"] if kind != "golddust" else DYE["gold"]
    out = np.zeros((SIZE, SIZE, 4), dtype=np.uint8)
    out[..., 0] = rgb[0]
    out[..., 1] = rgb[1]
    out[..., 2] = rgb[2]
    out[..., 3] = (mask.astype(np.float32) * (0.28 if kind != "golddust" else 0.55)).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def shift(points: list[tuple[float, float]], dx: float, dy: float) -> list[tuple[float, float]]:
    return [(x + dx, y + dy) for x, y in points]


def fold_geometry(kind: str, lift: float) -> dict[str, list[tuple[float, float]]]:
    """Angular paper facets. No ovals, no egg bodies, no dancing limbs."""
    if kind == "crane":
        return {
            "body": [(256, 236), (214, 292), (256, 338), (298, 292)],
            "neck": [(256, 236), (274, 188), (298, 154), (268, 176), (248, 228)],
            "head": [(298, 154), (328, 142), (312, 168)],
            "lwing": [(214, 292), (118, 248), (72, 214 + lift * 0.15), (196, 274)],
            "rwing": [(298, 292), (394, 248), (440, 200 - lift), (316, 270)],
            "tail": [(256, 338), (222, 408), (256, 382), (290, 408)],
        }
    if kind == "frog":
        return {
            "body": [(186, 228), (326, 228), (354, 292), (256, 348), (158, 292)],
            "belly": [(210, 268), (302, 268), (256, 330)],
            "lleg": [(158, 292), (96, 348 + lift * 0.3), (132, 372), (186, 318)],
            "rleg": [(354, 292), (416, 348 + lift * 0.3), (380, 372), (326, 318)],
            "lear": [(210, 228), (196, 188), (228, 214)],
            "rear": [(302, 228), (316, 188), (284, 214)],
        }
    if kind == "beetle":
        return {
            "thorax": [(216, 188), (296, 188), (318, 236), (194, 236)],
            "horn": [(256, 188), (244, 142 - lift * 0.4), (268, 142 - lift * 0.4)],
            "left": [(194, 236), (168, 318), (230, 368), (256, 300)],
            "right": [(318, 236), (344, 318), (282, 368), (256, 300)],
            "lleg": [(168, 318), (112, 346), (128, 360)],
            "rleg": [(344, 318), (400, 346), (384, 360)],
        }
    if kind == "boat":
        return {
            "hull": [(78, 292), (434, 292), (388, 362), (124, 362)],
            "lip": [(78, 292), (434, 292), (410, 318), (102, 318)],
            "mast": [(250, 292), (262, 292), (262, 128 - lift * 0.5), (250, 128 - lift * 0.5)],
            "sail": [(262, 136 - lift * 0.5), (262, 286), (368, 246)],
        }
    if kind == "hare":
        return {
            "body": [(200, 250), (312, 236), (340, 318), (256, 372), (176, 328)],
            "head": [(300, 200), (356, 188), (368, 230), (312, 248)],
            "lear": [(318, 188), (298, 112 - lift * 0.6), (336, 176)],
            "rear": [(348, 176), (372, 96 - lift), (380, 180)],
            "tail": [(176, 328), (148, 348), (176, 358)],
        }
    if kind == "fan":
        pivot = (256.0, 368.0)
        facets: dict[str, list[tuple[float, float]]] = {}
        for i in range(7):
            a0 = math.radians(198 + i * 18)
            a1 = math.radians(198 + (i + 1) * 18)
            r = 196 + (4 if i % 2 else 0) + (lift if i in (5, 6) else 0)
            facets[f"rib{i}"] = [
                pivot,
                (pivot[0] + math.cos(a0) * r, pivot[1] + math.sin(a0) * r),
                (pivot[0] + math.cos(a1) * r, pivot[1] + math.sin(a1) * r),
            ]
        facets["guard"] = [(232, 360), (280, 360), (286, 400), (226, 400)]
        return facets
    if kind == "kite":
        return {
            "sail": [(256, 118 - lift * 0.3), (348, 248), (256, 318), (164, 248)],
            "spine": [(250, 130), (262, 130), (262, 310), (250, 310)],
            "ltail": [(164, 248), (128, 330), (148, 400 + lift * 0.4), (176, 338)],
            "rtail": [(348, 248), (384, 330), (364, 400 + lift * 0.4), (336, 338)],
        }
    # lotus
    petals = {}
    for i, name in enumerate(("n", "ne", "se", "s", "sw", "nw")):
        a = i / 6 * math.tau - math.pi / 2
        extra = lift if name in ("ne", "se") else 0
        cx, cy = 256 + math.cos(a) * (78 + extra * 0.2), 248 + math.sin(a) * (70 + extra * 0.2)
        petals[name] = [
            (256, 248),
            (cx + math.cos(a - 0.5) * 54, cy + math.sin(a - 0.5) * 48),
            (cx + math.cos(a) * 88, cy + math.sin(a) * 78),
            (cx + math.cos(a + 0.5) * 54, cy + math.sin(a + 0.5) * 48),
        ]
    petals["heart"] = [(232, 228), (280, 228), (292, 268), (256, 292), (220, 268)]
    return petals


def draw_facet(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], rgb: tuple[int, int, int], dark: float) -> None:
    if len(points) < 3:
        return
    draw.polygon([(int(x), int(y)) for x, y in points], fill=rgb + (255,))
    # Fold shade — a thinner inner polygon, not a charcoal outline.
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    inner = [((x + cx) / 2, (y + cy) / 2) for x, y in points[: max(3, len(points) // 2 + 1)]]
    if len(inner) >= 3:
        draw.polygon([(int(x), int(y)) for x, y in inner], fill=shade(rgb, dark) + (90,))


def paint_fold(kind: str, frame: int, draft: str = "lift") -> Image.Image:
    if kind == "none":
        return blank()
    lift = lift_of(frame, draft)
    canvas = blank()
    draw = ImageDraw.Draw(canvas, "RGBA")
    dye = DYE[FOLD_DYE[kind]]
    facets = fold_geometry(kind, lift)
    # Draw back-to-front in dict order; shade alternates so facets read as paper planes.
    for index, points in enumerate(facets.values()):
        tone = 1.0 if index % 2 == 0 else 0.78
        draw_facet(draw, points, shade(dye, tone), 0.62)
    return canvas


def score_lines(kind: str) -> list[list[tuple[float, float]]]:
    if kind == "mountain":
        return [
            [(210, 250), (256, 200), (302, 250), (256, 330)],
            [(164, 270), (256, 236), (348, 270)],
        ]
    if kind == "valley":
        return [
            [(256, 150), (256, 360)],
            [(150, 250), (362, 250)],
            [(190, 190), (322, 320)],
        ]
    if kind == "diagram":
        return [
            [(256, 140), (256, 370)],
            [(140, 260), (372, 260)],
            [(176, 176), (336, 336)],
            [(336, 176), (176, 336)],
            [(200, 210), (312, 210), (312, 310), (200, 310), (200, 210)],
        ]
    if kind == "radial":
        lines = []
        for i in range(8):
            a = i / 8 * math.tau
            lines.append([(256, 250), (256 + math.cos(a) * 140, 250 + math.sin(a) * 130)])
        return lines
    # grid
    lines = []
    for x in range(160, 360, 28):
        lines.append([(x, 150), (x, 370)])
    for y in range(160, 370, 28):
        lines.append([(150, y), (362, y)])
    return lines


def dashed(draw: ImageDraw.ImageDraw, a: tuple[float, float], b: tuple[float, float], fill: tuple, width: int = 1) -> None:
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy) or 1
    steps = max(2, int(length / 7))
    for i in range(0, steps, 2):
        t0, t1 = i / steps, min(1.0, (i + 1) / steps)
        draw.line(
            [(a[0] + dx * t0, a[1] + dy * t0), (a[0] + dx * t1, a[1] + dy * t1)],
            fill=fill,
            width=width,
        )


def paint_score(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    canvas = blank()
    draw = ImageDraw.Draw(canvas, "RGBA")
    phase = math.sin(clock(frame)) * 2
    ink = (28, 26, 24, 170)
    for line in score_lines(kind):
        pts = [(x + phase, y) for x, y in line]
        if kind == "mountain":
            for a, b in zip(pts, pts[1:]):
                dashed(draw, a, b, ink, 1)
        else:
            draw.line([(int(x), int(y)) for x, y in pts], fill=ink, width=1)
        if kind == "diagram":
            for x, y in pts[::2]:
                draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(28, 26, 24, 140))
    return canvas


def paint_facet(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    t = clock(frame)
    canvas = blank()
    draw = ImageDraw.Draw(canvas, "RGBA")
    wash = {
        "wing": (196, 69, 45, 110),
        "body": (36, 52, 92, 100),
        "tip": (196, 156, 72, 120),
        "band": (74, 98, 62, 105),
        "gore": (232, 186, 156, 115),
    }[kind]
    if kind == "wing":
        pts = [(298, 250), (430, 188 + math.sin(t) * 6), (400, 280), (300, 300)]
    elif kind == "body":
        pts = [(210, 230), (302, 230), (330, 310), (256, 360), (182, 310)]
    elif kind == "tip":
        pts = [(300, 140), (350, 128), (330, 190)]
    elif kind == "band":
        pts = [(140, 268 + math.sin(t) * 3), (372, 250), (372, 286), (140, 304)]
    else:
        pts = [(256, 200), (320, 268), (256, 340), (192, 268)]
    draw.polygon([(int(x), int(y)) for x, y in pts], fill=wash)
    return canvas


def paint_seal(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    canvas = blank()
    draw = ImageDraw.Draw(canvas, "RGBA")
    verm = (180, 42, 36, 210)
    gold = (196, 156, 72, 200)
    if kind == "hanko":
        box = (368, 368, 452, 452)
        draw.rounded_rectangle(box, radius=6, outline=verm, width=3)
        draw.rounded_rectangle((376, 376, 444, 444), radius=4, outline=verm, width=2)
        draw.line([(392, 400), (428, 400)], fill=verm, width=3)
        draw.line([(410, 384), (410, 436)], fill=verm, width=3)
        draw.polygon([(396, 412), (410, 428), (424, 412)], outline=verm)
    elif kind == "twin":
        for i, x in enumerate((86, 118)):
            draw.arc((x, 380, x + 36, 448), 200, 520, fill=verm, width=3)
            draw.arc((x + 8, 388, x + 28, 440), 220, 500, fill=gold, width=2)
        draw.line([(104, 448), (104, 470)], fill=verm, width=2)
        draw.line([(136, 448), (136, 470)], fill=verm, width=2)
    elif kind == "loop":
        draw.arc((72, 72, 148, 148), 0, 360, fill=verm, width=4)
        draw.arc((88, 88, 132, 132), 0, 360, fill=gold, width=2)
    else:  # tassel
        draw.line([(400, 70), (400, 150)], fill=gold, width=2)
        draw.ellipse((388, 58, 412, 82), outline=verm, width=2)
        for i in range(5):
            a = math.radians(70 + i * 10)
            draw.line([(400, 150), (400 + math.cos(a) * 28, 188 + i * 2)], fill=verm, width=2)
    return canvas


def paint_draft(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    canvas = blank()
    draw = ImageDraw.Draw(canvas, "RGBA")
    t = clock(frame)
    lift = lift_of(frame, kind)
    # A loose corner catching air — paper, not a walking cancel.
    corner = [(428, 56), (478, 70 + lift * 0.4), (456, 124 + lift * 0.2), (412, 96)]
    draw.polygon([(int(x), int(y)) for x, y in corner], fill=(246, 240, 228, 150))
    draw.line([(428, 56), (456, 124 + lift * 0.2)], fill=(28, 26, 24, 80), width=1)
    if kind in ("scrap", "gust"):
        sx = 80 + math.sin(t) * 18
        sy = 120 + math.cos(t * 1.2) * 10
        scrap = [(sx, sy), (sx + 36, sy + 8), (sx + 28, sy + 28), (sx - 6, sy + 18)]
        draw.polygon([(int(x), int(y)) for x, y in scrap], fill=(196, 69, 45, 130))
    if kind == "gust":
        for i in range(4):
            y = 160 + i * 18 + math.sin(t + i) * 4
            draw.arc((40, y, 160, y + 24), 200, 340, fill=(246, 240, 228, 70), width=2)
    return canvas


# Painters for the studio stack keep fold motion independent of the draft layer
# by using a seated "lift" so the figure already breathes a little.
PAINTERS = {
    "pulp": {k: (lambda kind: (lambda frame, k=kind: paint_pulp(k, frame)))(k) for k in PULPS},
    "fleck": {k: (lambda kind: (lambda frame, k=kind: paint_fleck(k, frame)))(k) for k in FLECKS},
    "fold": {k: (lambda kind: (lambda frame, k=kind: paint_fold(k, frame, "lift")))(k) for k in FOLDS},
    "score": {k: (lambda kind: (lambda frame, k=kind: paint_score(k, frame)))(k) for k in SCORES},
    "facet": {k: (lambda kind: (lambda frame, k=kind: paint_facet(k, frame)))(k) for k in FACETS},
    "seal": {k: (lambda kind: (lambda frame, k=kind: paint_seal(k, frame)))(k) for k in SEALS},
    "draft": {k: (lambda kind: (lambda frame, k=kind: paint_draft(k, frame)))(k) for k in DRAFTS},
}

STACK = ("pulp", "fleck", "fold", "score", "facet", "seal", "draft")

TRAIT_SPEC: dict[str, list[tuple[str, str, int]]] = {
    "pulp": [
        ("cream", "Cream Washi", 18),
        ("indigo", "Indigo Washi", 14),
        ("vermilion", "Vermilion Washi", 12),
        ("moss", "Moss Washi", 12),
        ("peach", "Peach Washi", 12),
        ("gold", "Gold Washi", 12),
        ("ink", "Ink Washi", 10),
        ("frost", "Frost Washi", 10),
    ],
    "fleck": [
        ("none", "Plain Sheet", 24),
        ("kozo", "Kozo Fiber", 18),
        ("golddust", "Gold Dust", 16),
        ("speckle", "Speckle", 16),
        ("stripe", "Laid Stripe", 14),
        ("cloud", "Cloud Wash", 12),
    ],
    "fold": [
        ("crane", "Crane", 18),
        ("frog", "Frog", 16),
        ("beetle", "Beetle", 14),
        ("boat", "Boat", 14),
        ("hare", "Hare", 12),
        ("fan", "Fan", 10),
        ("kite", "Kite", 8),
        ("lotus", "Lotus", 8),
    ],
    "score": [
        ("none", "No Score", 22),
        ("mountain", "Mountain Fold", 18),
        ("valley", "Valley Fold", 18),
        ("diagram", "Crease Diagram", 16),
        ("radial", "Radial Score", 14),
        ("grid", "Grid Score", 12),
    ],
    "facet": [
        ("none", "Bare Facet", 24),
        ("wing", "Wing Wash", 18),
        ("body", "Body Wash", 16),
        ("tip", "Tip Wash", 16),
        ("band", "Band Wash", 14),
        ("gore", "Gore Wash", 12),
    ],
    "seal": [
        ("none", "No Seal", 26),
        ("hanko", "Hanko", 20),
        ("twin", "Twin Cord", 18),
        ("loop", "Mizuhiki Loop", 18),
        ("tassel", "Tassel", 18),
    ],
    "draft": [
        ("none", "Still Air", 22),
        ("lift", "Corner Lift", 22),
        ("flutter", "Flutter", 20),
        ("scrap", "Loose Scrap", 18),
        ("gust", "Gust", 18),
    ],
}

SIGNATURES = [
    {"pulp": "cream", "fleck": "kozo", "fold": "crane", "score": "mountain", "facet": "none", "seal": "hanko", "draft": "lift"},
    {"pulp": "indigo", "fleck": "golddust", "fold": "frog", "score": "valley", "facet": "body", "seal": "twin", "draft": "flutter"},
    {"pulp": "moss", "fleck": "none", "fold": "beetle", "score": "diagram", "facet": "band", "seal": "loop", "draft": "none"},
    {"pulp": "peach", "fleck": "speckle", "fold": "hare", "score": "none", "facet": "tip", "seal": "none", "draft": "scrap"},
    {"pulp": "gold", "fleck": "stripe", "fold": "boat", "score": "valley", "facet": "wing", "seal": "tassel", "draft": "gust"},
    {"pulp": "vermilion", "fleck": "cloud", "fold": "fan", "score": "radial", "facet": "gore", "seal": "hanko", "draft": "lift"},
    {"pulp": "frost", "fleck": "kozo", "fold": "kite", "score": "grid", "facet": "none", "seal": "twin", "draft": "flutter"},
    {"pulp": "ink", "fleck": "golddust", "fold": "lotus", "score": "mountain", "facet": "body", "seal": "loop", "draft": "none"},
    {"pulp": "cream", "fleck": "none", "fold": "boat", "score": "diagram", "facet": "band", "seal": "none", "draft": "scrap"},
    {"pulp": "indigo", "fleck": "speckle", "fold": "crane", "score": "none", "facet": "wing", "seal": "tassel", "draft": "gust"},
    {"pulp": "moss", "fleck": "stripe", "fold": "hare", "score": "radial", "facet": "tip", "seal": "hanko", "draft": "lift"},
    {"pulp": "peach", "fleck": "cloud", "fold": "frog", "score": "grid", "facet": "none", "seal": "twin", "draft": "flutter"},
    {"pulp": "gold", "fleck": "kozo", "fold": "lotus", "score": "valley", "facet": "gore", "seal": "none", "draft": "none"},
    {"pulp": "vermilion", "fleck": "golddust", "fold": "kite", "score": "mountain", "facet": "body", "seal": "loop", "draft": "scrap"},
    {"pulp": "frost", "fleck": "none", "fold": "beetle", "score": "diagram", "facet": "wing", "seal": "tassel", "draft": "gust"},
    {"pulp": "ink", "fleck": "speckle", "fold": "fan", "score": "none", "facet": "band", "seal": "hanko", "draft": "lift"},
]

TRAIT_LABELS = (
    ("pulp", "Pulp"),
    ("fleck", "Fleck"),
    ("fold", "Fold"),
    ("score", "Score"),
    ("facet", "Facet"),
    ("seal", "Seal"),
    ("draft", "Draft"),
)

COLLECTION_DESCRIPTION = (
    "Kamiori is an 8,888-piece collection of looping origami PFP GIFs. "
    "Each sheet is stacked from seven plates — pulp, fleck, fold, score, facet, seal, and draft — "
    "then flattened onto one 12-frame GIF. Polygonal facets. Valley and mountain scores. A corner that lifts."
)

COLLECTION_STORY = (
    "Kamiori.\n\n"
    "An 8,888-piece collection of looping origami PFP GIFs on Robinhood Chain. "
    "Each sheet is stacked from seven plates — pulp, fleck, fold, score, facet, seal, and draft — "
    "then flattened onto one 12-frame GIF. Eight folds, each its own washi dye: crane, frog, beetle, boat, "
    "hare, fan, kite, and lotus. A crease diagram sits on the paper. A draft lifts one corner.\n\n"
    "Deckle washi. Angular facets. No engraved bust. No perforated stamp. "
    "No charcoal outline. No sticker cutout. The fold stays seated. One shared clock.\n\n"
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
        "name": "Kamiori",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Eight origami folds share one envelope; seals and drafts never edit the fold file.",
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
                "name": f"Fold #{index}",
                "image": f"/kamiori-preview/{index}.gif",
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
    (SRC_DATA / "kamiori-gallery.ts").write_text(
        "export type KamioriSample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const kamioriSamples: KamioriSample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def write_ts_traits() -> None:
    blurbs = {
        "pulp": "Deckle washi — cream, indigo, vermilion, moss, peach, gold, ink, frost.",
        "fleck": "Paper tooth — kozo fiber, gold dust, speckle, laid stripe, cloud wash — or a plain sheet.",
        "fold": "The seated origami. Eight folds: crane, frog, beetle, boat, hare, fan, kite, lotus.",
        "score": "Crease language — mountain, valley, diagram, radial, grid — or unmarked paper.",
        "facet": "A second dye on one plane — wing, body, tip, band, gore — or a bare facet.",
        "seal": "A mark that stays put — hanko, twin cord, mizuhiki loop, tassel — or no seal.",
        "draft": "Air on the sheet — corner lift, flutter, loose scrap, gust — or still air.",
    }
    none_labels = {
        "fleck": "Plain Sheet",
        "score": "No Score",
        "facet": "Bare Facet",
        "seal": "No Seal",
        "draft": "Still Air",
    }
    cats = []
    for key, label in TRAIT_LABELS:
        traits = []
        for trait_id, name, rarity in TRAIT_SPEC[key]:
            if trait_id == "none":
                continue
            traits.append(
                "      { "
                f'id: "{trait_id}", name: "{name}", image: "/kamiori-traits/{key}/{trait_id}.png", rarity: {rarity} '
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
    (SRC_DATA / "kamiori-traits.ts").write_text(
        "export type KamioriTrait = {\n"
        "  id: string;\n"
        "  name: string;\n"
        "  image?: string;\n"
        "  rarity: number;\n"
        "};\n\n"
        "export type KamioriTraitCategory = {\n"
        f"  id: {ids};\n"
        "  label: string;\n"
        "  blurb: string;\n"
        "  noneLabel?: string;\n"
        "  traits: KamioriTrait[];\n"
        "};\n\n"
        "/** Bump when APNG layers change so the studio does not keep a stale loop. */\n"
        'export const KAMIORI_ART_VERSION = "kamiori-v1";\n\n'
        "export const KAMIORI_FRAMES = 12;\n"
        "export const KAMIORI_DURATION_MS = 90;\n\n"
        "export function kamioriTraitSrc(path?: string) {\n"
        "  if (!path) return \"\";\n"
        "  return `${path}?v=${KAMIORI_ART_VERSION}`;\n"
        "}\n\n"
        "export const kamioriTraitCategories: KamioriTraitCategory[] = [\n"
        + ",\n".join(cats)
        + "\n];\n\n"
        'export const noneKamioriTrait: KamioriTrait = { id: "none", name: "None", rarity: 0 };\n\n'
        "export function kamioriCategoryById(id: KamioriTraitCategory[\"id\"]) {\n"
        "  const category = kamioriTraitCategories.find((item) => item.id === id);\n"
        "  if (!category) throw new Error(`Unknown Kamiori trait category: ${id}`);\n"
        "  return category;\n"
        "}\n\n"
        "export function findKamioriTrait(categoryId: KamioriTraitCategory[\"id\"], traitId: string) {\n"
        "  if (traitId === \"none\") return noneKamioriTrait;\n"
        "  return kamioriCategoryById(categoryId).traits.find((trait) => trait.id === traitId);\n"
        "}\n\n"
        "export const defaultKamioriSelection = {\n"
        '  pulp: "cream",\n'
        '  fleck: "kozo",\n'
        '  fold: "crane",\n'
        '  score: "mountain",\n'
        '  facet: "none",\n'
        '  seal: "hanko",\n'
        '  draft: "lift",\n'
        "} as const;\n\n"
        "export type KamioriSelection = Record<KamioriTraitCategory[\"id\"], string>;\n\n"
        "export function randomKamioriSelection(): KamioriSelection {\n"
        "  const pick = (category: KamioriTraitCategory) => {\n"
        "    const pool: KamioriTrait[] = category.noneLabel\n"
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
        '    pulp: pick(kamioriCategoryById("pulp")),\n'
        '    fleck: pick(kamioriCategoryById("fleck")),\n'
        '    fold: pick(kamioriCategoryById("fold")),\n'
        '    score: pick(kamioriCategoryById("score")),\n'
        '    facet: pick(kamioriCategoryById("facet")),\n'
        '    seal: pick(kamioriCategoryById("seal")),\n'
        '    draft: pick(kamioriCategoryById("draft")),\n'
        "  };\n"
        "}\n\n"
        "export function kamioriCombinationCount() {\n"
        "  return kamioriTraitCategories.reduce((product, category) => {\n"
        "    const extra = category.noneLabel ? 1 : 0;\n"
        "    return product * (category.traits.length + extra);\n"
        "  }, 1);\n"
        "}\n\n"
        "export function kamioriSelectionToLayers(selection: KamioriSelection) {\n"
        '  return (["pulp", "fleck", "fold", "score", "facet", "seal", "draft"] as const)\n'
        "    .map((id) => findKamioriTrait(id, selection[id]))\n"
        "    .filter((trait): trait is KamioriTrait => Boolean(trait?.image))\n"
        "    .map((trait) => kamioriTraitSrc(trait.image));\n"
        "}\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array(
        [
            [0.96, 0.94, 0.89],
            [0.77, 0.27, 0.18],
            [0.14, 0.20, 0.36],
            [0.29, 0.38, 0.24],
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
    (META_DIR / "kamiori-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "kamiori.json").write_text(
        json.dumps(
            {
                "name": "Kamiori",
                "symbol": "KMIO",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-kamiori.gif",
                "featured_image": "/brand/featured-kamiori.jpg",
                "banner_image": "/brand/banner-kamiori.png",
                "opensea_banner_image": "/brand/banner-kamiori-opensea.jpg",
                "external_link": "/kamiori",
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
        (12, 12, SIZE - 13, SIZE - 13), radius=40, outline=(196, 69, 45, 255), width=4
    )
    logo = Image.alpha_composite(logo, rim)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-kamiori.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-kamiori-loop.png",
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

    save_image(lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-kamiori.png", quality=94)
    save_image(lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-kamiori-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=28)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=28)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-kamiori.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(
        gif_frames,
        BRAND_DIR / "collection-kamiori.gif",
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
        print("Writing Kamiori brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Kamiori origami sheets…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
