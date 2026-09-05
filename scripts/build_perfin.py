#!/usr/bin/env python3
"""Paint Perfin — engraved postage-stamp characters.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
The bust stays seated in one vignette. A cancellation walks the face.
Hatch is the drawing language: parallel intaglio lines, not blobs,
not charcoal contours, not sticker cutouts, not glass, not notes.

Look: a perforated rectangle. Eight engraved postal busts. Classic
stamp inks. Guilloche behind the portrait. A surcharge that overprints.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gif_bake import save_loop_gif  # noqa: E402
from paint_kit import DURATION_MS, FRAMES, SIZE, place_portrait, save_apng, save_image  # noqa: E402

GIF_COLORS = 128
GIF_DITHER = Image.Dither.NONE

TRAIT_DIR = ROOT / "public" / "perfin-traits"
PREVIEW_DIR = ROOT / "public" / "perfin-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

WOVES = ("ivory", "rose", "azure", "buff", "lilac", "sage", "pearl", "grey")
GUILLOCHES = ("rose", "engine", "lattice", "sunburst", "wave", "tablet")
BUSTS = ("pilot", "keeper", "clerk", "captain", "botanist", "mapper", "signal", "warden")
SURCHARGES = ("none", "bar", "band", "triangle", "oval")
ASPECTS = ("calm", "stern", "wink", "shout", "glance", "smile")
DEVICES = ("none", "goggles", "specs", "medal", "pipe", "cockade")
CANCELS = ("none", "cds", "waves", "mute", "bars")

# Classic postage inks. Not a house palette and not risograph fluorescents.
INK = {
    "carmine": (155, 36, 54),
    "prussian": (27, 54, 93),
    "viridian": (22, 92, 68),
    "violet": (88, 42, 110),
    "sepia": (92, 58, 32),
    "orange": (184, 86, 28),
    "black": (28, 26, 24),
    "slate": (58, 70, 82),
}

PAPER = {
    "ivory": (243, 236, 220),
    "rose": (240, 220, 218),
    "azure": (220, 228, 234),
    "buff": (232, 214, 186),
    "lilac": (228, 220, 230),
    "sage": (220, 228, 214),
    "pearl": (234, 232, 228),
    "grey": (214, 214, 210),
}

BUST_INK = {
    "pilot": "prussian",
    "keeper": "sepia",
    "clerk": "violet",
    "captain": "carmine",
    "botanist": "viridian",
    "mapper": "orange",
    "signal": "slate",
    "warden": "black",
}

SURCHARGE_INK = {
    "bar": "carmine",
    "band": "prussian",
    "triangle": "orange",
    "oval": "violet",
}

MARGIN = 36
PERF_R = 5
PERF_STEP = 16
INNER = (MARGIN + 10, MARGIN + 10, SIZE - MARGIN - 11, SIZE - MARGIN - 11)


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def clock(frame: int) -> float:
    return frame / FRAMES * math.tau


def seed_for(*parts: object) -> int:
    payload = "|".join(map(str, parts)).encode()
    return int(hashlib.md5(payload).hexdigest()[:8], 16)


def empty_mask() -> np.ndarray:
    return np.zeros((SIZE, SIZE), dtype=np.uint8)


def or_mask(base: np.ndarray, add: np.ndarray) -> np.ndarray:
    return np.maximum(base, add)


def ellipse_mask(cx: float, cy: float, rx: float, ry: float, rot: float = 0.0) -> np.ndarray:
    stamp = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(stamp).ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    if abs(rot) > 1e-4:
        stamp = stamp.rotate(-math.degrees(rot), resample=Image.Resampling.BILINEAR, center=(cx, cy))
    return np.asarray(stamp, dtype=np.uint8)


def poly_mask(points: list[tuple[float, float]]) -> np.ndarray:
    layer = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(layer).polygon([(int(round(x)), int(round(y))) for x, y in points], fill=255)
    return np.asarray(layer, dtype=np.uint8)


def capsule_mask(x0: float, y0: float, x1: float, y1: float, radius: float) -> np.ndarray:
    layer = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(layer)
    width = max(2, int(round(radius * 2)))
    draw.line([(x0, y0), (x1, y1)], fill=255, width=width)
    draw.ellipse((x0 - radius, y0 - radius, x0 + radius, y0 + radius), fill=255)
    draw.ellipse((x1 - radius, y1 - radius, x1 + radius, y1 + radius), fill=255)
    return np.asarray(layer, dtype=np.uint8)


def stamp_window() -> np.ndarray:
    layer = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(layer).rectangle(INNER, fill=255)
    return np.asarray(layer, dtype=np.uint8)


def perforation_holes() -> np.ndarray:
    holes = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(holes)
    left, top, right, bottom = MARGIN, MARGIN, SIZE - MARGIN - 1, SIZE - MARGIN - 1
    for x in range(left, right + 1, PERF_STEP):
        draw.ellipse((x - PERF_R, top - PERF_R, x + PERF_R, top + PERF_R), fill=255)
        draw.ellipse((x - PERF_R, bottom - PERF_R, x + PERF_R, bottom + PERF_R), fill=255)
    for y in range(top + PERF_STEP, bottom, PERF_STEP):
        draw.ellipse((left - PERF_R, y - PERF_R, left + PERF_R, y + PERF_R), fill=255)
        draw.ellipse((right - PERF_R, y - PERF_R, right + PERF_R, y + PERF_R), fill=255)
    return np.asarray(holes, dtype=np.uint8)


def hatch(mask: np.ndarray, angle: float, spacing: float, phase: float, weight: float = 0.9) -> np.ndarray:
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    proj = xx * math.cos(angle) + yy * math.sin(angle) + phase
    band = np.abs(np.mod(proj, spacing) - spacing * 0.5)
    lines = (band < weight) & (mask > 28)
    out = np.zeros((SIZE, SIZE), dtype=np.uint8)
    out[lines] = np.clip(mask[lines], 0, 255)
    return out


def engrave(mask: np.ndarray, frame: int, density: float = 1.0, angle: float = 0.72) -> np.ndarray:
    """Intaglio tone: parallel hatch, cross-hatch in the darker core."""
    t = clock(frame)
    phase = math.sin(t) * 1.2
    spacing = max(2.6, 3.6 / density)
    tone = hatch(mask, angle, spacing, phase, 0.85)
    core = mask > 170
    if np.any(core):
        cross = hatch((core.astype(np.uint8) * 255), angle + 1.15, spacing * 1.15, -phase, 0.7)
        tone = or_mask(tone, cross)
    rim = Image.fromarray(mask, "L").filter(ImageFilter.FIND_EDGES)
    rim_arr = np.asarray(rim, dtype=np.uint8)
    rim_h = hatch(rim_arr, angle + 0.2, 2.4, phase * 0.4, 0.7)
    return or_mask(tone, rim_h)


def plate(mask: np.ndarray, rgb: tuple[int, int, int], opacity: float = 0.92) -> Image.Image:
    out = np.zeros((SIZE, SIZE, 4), dtype=np.uint8)
    out[..., 0] = rgb[0]
    out[..., 1] = rgb[1]
    out[..., 2] = rgb[2]
    out[..., 3] = np.clip(mask.astype(np.float32) * opacity, 0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def paint_wove(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    base = np.array(PAPER[kind], dtype=np.float32)
    rng = np.random.RandomState(seed_for("wove", kind))
    laid = rng.randn(SIZE, SIZE).astype(np.float32) * 2.4
    yy = np.linspace(0, 1, SIZE, dtype=np.float32)[:, None]
    fade = (1.0 - yy * 0.04) * 255.0
    rgb = np.clip(base + laid[..., None], 0, 255).astype(np.uint8)
    alpha = np.zeros((SIZE, SIZE), dtype=np.uint8)
    body = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(body).rectangle((MARGIN, MARGIN, SIZE - MARGIN - 1, SIZE - MARGIN - 1), fill=255)
    alpha = np.asarray(body, dtype=np.uint8)
    holes = perforation_holes()
    alpha = np.where(holes > 80, 0, alpha)
    # Laid lines — a paper tooth, not riso grain.
    t = clock(frame)
    laid_lines = hatch(alpha, 0.0, 7.0, math.sin(t) * 0.4, 0.35)
    rgb = rgb.copy()
    shade = (laid_lines > 0).astype(np.float32) * 6.0
    rgb = np.clip(rgb.astype(np.float32) - shade[..., None], 0, 255).astype(np.uint8)
    out = np.dstack([rgb, np.clip(alpha.astype(np.float32) * (fade / 255.0), 0, 255).astype(np.uint8)])
    return Image.fromarray(out, "RGBA")


def paint_guilloche(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    window = stamp_window()
    t = clock(frame)
    cx, cy = 256.0, 236.0
    layer = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(layer)
    if kind == "rose":
        for i in range(18):
            a = t * 0.08 + i * 0.35
            rx, ry = 118 + (i % 5) * 8, 148 - (i % 4) * 6
            box = (cx - rx + math.cos(a) * 2, cy - ry, cx + rx + math.cos(a) * 2, cy + ry)
            draw.ellipse(box, outline=210, width=1)
    elif kind == "engine":
        for i in range(40):
            a = i / 40 * math.tau + t * 0.05
            r = 70 + 48 * math.sin(3 * a + t * 0.2)
            x = cx + math.cos(a) * r
            y = cy + math.sin(a) * r * 1.15
            if i:
                draw.line([(px, py), (x, y)], fill=200, width=1)
            px, py = x, y
    elif kind == "lattice":
        for x in range(int(INNER[0]), int(INNER[2]), 14):
            draw.line([(x + math.sin(t) * 2, INNER[1]), (x - 40, INNER[3])], fill=170, width=1)
        for y in range(int(INNER[1]), int(INNER[3]), 16):
            draw.line([(INNER[0], y), (INNER[2], y + 10)], fill=150, width=1)
    elif kind == "sunburst":
        for i in range(36):
            a = i / 36 * math.tau + t * 0.03
            draw.line(
                [(cx, cy), (cx + math.cos(a) * 200, cy + math.sin(a) * 220)],
                fill=180,
                width=1,
            )
    elif kind == "wave":
        for row in range(int(INNER[1]) + 8, int(INNER[3]) - 8, 10):
            pts = []
            for x in range(int(INNER[0]), int(INNER[2]), 6):
                pts.append((x, row + math.sin(x * 0.06 + t + row * 0.02) * 4))
            draw.line(pts, fill=190, width=1)
    else:  # tablet
        draw.rounded_rectangle((70, 54, 442, 100), radius=8, outline=210, width=2)
        draw.rounded_rectangle((70, 400, 442, 456), radius=8, outline=210, width=2)
        try:
            font = ImageFont.load_default()
        except OSError:
            font = None
        draw.text((96, 66), "PERFIN POST", fill=220, font=font)
        draw.text((200, 418), "25c", fill=220, font=font)

    mask = np.minimum(np.asarray(layer, dtype=np.uint8), window)
    # Keep guilloche faint — security engraving, not a wash.
    return plate(mask, INK["slate"], opacity=0.42)


def bust_mask(kind: str, frame: int) -> np.ndarray:
    """Seated engraved bust. Head and shoulders share one vignette."""
    hx, hy = 256.0, 186.0
    mask = empty_mask()
    # Shoulders — a coat wedge, not an egg and not dancing limbs.
    if kind == "pilot":
        mask = or_mask(mask, ellipse_mask(hx, hy - 6, 46, 50))
        mask = or_mask(mask, ellipse_mask(hx, hy - 28, 50, 18))  # helmet dome
        mask = or_mask(
            mask,
            poly_mask([(hx - 92, 360), (hx - 58, 268), (hx + 58, 268), (hx + 96, 360), (hx, 378)]),
        )
    elif kind == "keeper":
        mask = or_mask(mask, ellipse_mask(hx, hy + 4, 42, 48))
        mask = or_mask(mask, ellipse_mask(hx, hy + 36, 28, 22))  # beard
        mask = or_mask(mask, ellipse_mask(hx, hy - 34, 48, 14))  # flat cap
        mask = or_mask(
            mask,
            poly_mask([(hx - 88, 358), (hx - 50, 274), (hx + 52, 274), (hx + 90, 358), (hx, 372)]),
        )
    elif kind == "clerk":
        mask = or_mask(mask, ellipse_mask(hx, hy, 40, 46))
        mask = or_mask(mask, ellipse_mask(hx - 38, hy + 6, 10, 16))  # ear
        mask = or_mask(mask, ellipse_mask(hx + 38, hy + 6, 10, 16))
        mask = or_mask(
            mask,
            poly_mask([(hx - 70, 350), (hx - 40, 278), (hx + 40, 278), (hx + 70, 350), (hx, 364)]),
        )
        mask = or_mask(mask, poly_mask([(hx - 28, 300), (hx, 338), (hx + 28, 300)]))  # collar
    elif kind == "captain":
        mask = or_mask(mask, ellipse_mask(hx, hy, 44, 48))
        mask = or_mask(mask, ellipse_mask(hx, hy - 32, 56, 16))
        mask = or_mask(mask, ellipse_mask(hx + 18, hy - 18, 40, 8, 0.15))  # visor
        mask = or_mask(
            mask,
            poly_mask([(hx - 100, 362), (hx - 60, 270), (hx + 60, 270), (hx + 104, 362), (hx, 380)]),
        )
    elif kind == "botanist":
        mask = or_mask(mask, ellipse_mask(hx, hy + 2, 40, 46))
        mask = or_mask(mask, ellipse_mask(hx - 8, hy - 36, 36, 20, -0.3))
        mask = or_mask(mask, ellipse_mask(hx + 22, hy - 28, 22, 16, 0.5))
        mask = or_mask(
            mask,
            poly_mask([(hx - 80, 354), (hx - 48, 276), (hx + 48, 276), (hx + 82, 354), (hx, 368)]),
        )
    elif kind == "mapper":
        mask = or_mask(mask, ellipse_mask(hx + 4, hy + 2, 38, 46))
        mask = or_mask(mask, ellipse_mask(hx + 10, hy - 20, 36, 16))  # high brow
        mask = or_mask(
            mask,
            poly_mask([(hx - 86, 356), (hx - 44, 276), (hx + 56, 276), (hx + 94, 356), (hx + 8, 370)]),
        )
        mask = or_mask(mask, ellipse_mask(hx + 48, 320, 28, 10, 0.6))  # chart roll
    elif kind == "signal":
        mask = or_mask(mask, ellipse_mask(hx, hy, 42, 44))
        mask = or_mask(mask, ellipse_mask(hx, hy - 30, 40, 12))
        mask = or_mask(
            mask,
            poly_mask([(hx - 84, 352), (hx - 52, 274), (hx + 52, 274), (hx + 86, 352), (hx, 366)]),
        )
    else:  # warden
        mask = or_mask(mask, ellipse_mask(hx, hy + 6, 46, 50))
        mask = or_mask(mask, ellipse_mask(hx, hy + 28, 30, 10))  # mustache mass
        mask = or_mask(
            mask,
            poly_mask([(hx - 78, 348), (hx - 36, 268), (hx + 36, 268), (hx + 80, 348), (hx, 360)]),
        )
        mask = or_mask(mask, ellipse_mask(hx, 292, 34, 18))  # tall collar

    oval = ellipse_mask(256, 232, 132, 168)
    return np.minimum(mask, oval)


def paint_bust(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    rgb = INK[BUST_INK[kind]]
    mask = bust_mask(kind, frame)
    engraved = engrave(mask, frame, density=1.15 if kind in ("warden", "captain") else 1.0)
    return plate(engraved, rgb, opacity=0.94)


def paint_surcharge(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    t = clock(frame)
    shift = math.sin(t) * 3
    window = stamp_window()
    mask = empty_mask()
    if kind == "bar":
        mask = or_mask(mask, poly_mask([(64, 300 + shift), (448, 288 + shift), (448, 312 + shift), (64, 324 + shift)]))
    elif kind == "band":
        mask = or_mask(
            mask,
            poly_mask([(70, 90 + shift), (442, 140 + shift), (442, 168 + shift), (70, 118 + shift)]),
        )
    elif kind == "triangle":
        mask = or_mask(mask, poly_mask([(360, 64), (448, 64), (448, 152)]))
    else:
        mask = or_mask(mask, ellipse_mask(256 + shift, 230, 78, 54, 0.2))
    mask = np.minimum(mask, window)
    engraved = hatch(mask, 0.15, 3.2, t * 2, 0.8)
    return plate(or_mask(engraved, hatch(mask, 1.4, 4.0, -t, 0.55)), INK[SURCHARGE_INK[kind]], opacity=0.62)


def paint_aspect(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    hx, hy = 256.0, 186.0
    blink = 1.0 if frame % 12 not in (4,) else 0.25
    mask = empty_mask()
    if kind in ("calm", "stern", "shout", "smile", "glance"):
        ly, ry = (hx - 16, hx + 18) if kind != "glance" else (hx - 12, hx + 22)
        mask = or_mask(mask, ellipse_mask(ly, hy - 2, 5.5, 6.5 * blink + 1.2))
        mask = or_mask(mask, ellipse_mask(ry, hy - 2, 5.5, 6.5 * blink + 1.2))
    if kind == "wink":
        mask = or_mask(mask, ellipse_mask(hx - 16, hy - 2, 5.5, 6.5 * blink + 1.2))
        mask = or_mask(mask, ellipse_mask(hx + 18, hy - 1, 8, 2.2))
    if kind == "stern":
        mask = or_mask(mask, capsule_mask(hx - 22, hy - 14, hx - 8, hy - 10, 1.6))
        mask = or_mask(mask, capsule_mask(hx + 8, hy - 14, hx + 24, hy - 10, 1.6))
        mask = or_mask(mask, capsule_mask(hx - 10, hy + 18, hx + 10, hy + 18, 1.8))
    if kind == "calm":
        mask = or_mask(mask, capsule_mask(hx - 8, hy + 18, hx + 8, hy + 18, 1.6))
    if kind == "smile":
        mask = or_mask(mask, capsule_mask(hx - 12, hy + 16, hx + 12, hy + 20, 1.8))
    if kind == "shout":
        mask = or_mask(mask, ellipse_mask(hx, hy + 18, 7, 9))
    if kind == "glance":
        mask = or_mask(mask, capsule_mask(hx - 6, hy + 16, hx + 10, hy + 16, 1.5))
    engraved = engrave(mask, frame, density=1.6, angle=0.4)
    return plate(or_mask(engraved, mask), INK["black"], opacity=0.9)


def paint_device(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    hx, hy = 256.0, 186.0
    mask = empty_mask()
    if kind == "goggles":
        mask = or_mask(mask, ellipse_mask(hx - 16, hy - 2, 14, 11))
        mask = or_mask(mask, ellipse_mask(hx + 18, hy - 2, 14, 11))
        mask = or_mask(mask, capsule_mask(hx - 2, hy - 2, hx + 4, hy - 2, 2))
        hollow = or_mask(ellipse_mask(hx - 16, hy - 2, 8, 6), ellipse_mask(hx + 18, hy - 2, 8, 6))
        mask = np.where(hollow > 80, 0, mask)
    elif kind == "specs":
        mask = or_mask(mask, ellipse_mask(hx - 15, hy, 12, 10))
        mask = or_mask(mask, ellipse_mask(hx + 17, hy, 12, 10))
        mask = or_mask(mask, capsule_mask(hx - 3, hy, hx + 5, hy, 1.4))
        hollow = or_mask(ellipse_mask(hx - 15, hy, 8, 6), ellipse_mask(hx + 17, hy, 8, 6))
        mask = np.where(hollow > 80, 0, mask)
    elif kind == "medal":
        mask = or_mask(mask, ellipse_mask(hx, 318, 16, 16))
        mask = or_mask(mask, poly_mask([(hx - 8, 300), (hx, 312), (hx + 8, 300), (hx, 292)]))
        mask = or_mask(mask, ellipse_mask(hx, 318, 8, 8))
    elif kind == "pipe":
        mask = or_mask(mask, capsule_mask(hx + 10, hy + 20, hx + 48, hy + 28, 3))
        mask = or_mask(mask, ellipse_mask(hx + 54, hy + 22, 10, 8))
    else:  # cockade
        mask = or_mask(mask, ellipse_mask(hx - 40, hy - 30, 12, 12))
        mask = or_mask(mask, ellipse_mask(hx - 40, hy - 30, 6, 6))
    engraved = engrave(mask, frame, density=1.3, angle=0.95)
    return plate(or_mask(engraved, hatch(mask, 0.95, 2.8, 0, 0.7)), INK["black"], opacity=0.88)


def paint_cancel(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    t = clock(frame)
    walk_x = math.sin(t) * 22
    walk_y = math.cos(t * 0.85) * 10
    layer = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(layer)
    if kind == "cds":
        cx, cy = 300 + walk_x, 200 + walk_y
        draw.ellipse((cx - 58, cy - 58, cx + 58, cy + 58), outline=230, width=3)
        draw.ellipse((cx - 42, cy - 42, cx + 42, cy + 42), outline=200, width=1)
        try:
            font = ImageFont.load_default()
        except OSError:
            font = None
        draw.text((cx - 28, cy - 6), "PERFIN", fill=220, font=font)
    elif kind == "waves":
        phase = t * 8 + walk_x
        for i in range(7):
            y = 150 + i * 28 + walk_y * 0.3
            pts = [(x, y + math.sin(x * 0.08 + phase) * 5) for x in range(48, 470, 5)]
            draw.line(pts, fill=220, width=2)
    elif kind == "mute":
        draw.ellipse((210 + walk_x, 160 + walk_y, 390 + walk_x, 300 + walk_y), fill=200)
    else:  # bars
        for i in range(5):
            y = 168 + i * 26 + walk_y * 0.4
            draw.rectangle((70, y, 442, y + 7), fill=210)
    mask = np.minimum(np.asarray(layer, dtype=np.uint8), stamp_window())
    return plate(mask, INK["black"], opacity=0.48 if kind != "mute" else 0.28)


TRAIT_SPEC: dict[str, list[tuple[str, str, int]]] = {
    "wove": [
        ("ivory", "Ivory Wove", 18),
        ("rose", "Rose Wove", 14),
        ("azure", "Azure Wove", 12),
        ("buff", "Buff Wove", 12),
        ("lilac", "Lilac Wove", 12),
        ("sage", "Sage Wove", 12),
        ("pearl", "Pearl Wove", 10),
        ("grey", "Grey Wove", 10),
    ],
    "guilloche": [
        ("rose", "Rose Engine", 18),
        ("engine", "Geometric Engine", 16),
        ("lattice", "Lattice", 16),
        ("sunburst", "Sunburst", 14),
        ("wave", "Wave Engine", 14),
        ("tablet", "Value Tablet", 12),
    ],
    "bust": [
        ("pilot", "Pilot", 18),
        ("keeper", "Keeper", 16),
        ("clerk", "Clerk", 14),
        ("captain", "Captain", 14),
        ("botanist", "Botanist", 12),
        ("mapper", "Mapper", 10),
        ("signal", "Signal", 8),
        ("warden", "Warden", 8),
    ],
    "surcharge": [
        ("none", "No Surcharge", 28),
        ("bar", "Carmine Bar", 18),
        ("band", "Prussian Band", 16),
        ("triangle", "Orange Triangle", 14),
        ("oval", "Violet Oval", 12),
    ],
    "aspect": [
        ("calm", "Calm", 22),
        ("stern", "Stern", 18),
        ("wink", "Wink", 16),
        ("shout", "Shout", 16),
        ("glance", "Glance", 14),
        ("smile", "Smile", 14),
    ],
    "device": [
        ("none", "Bare Device", 28),
        ("goggles", "Goggles", 18),
        ("specs", "Spectacles", 16),
        ("medal", "Medal", 14),
        ("pipe", "Pipe", 12),
        ("cockade", "Cockade", 12),
    ],
    "cancel": [
        ("none", "Mint Uncancelled", 26),
        ("cds", "Circular Date", 20),
        ("waves", "Wavy Lines", 18),
        ("mute", "Mute Killer", 14),
        ("bars", "Killer Bars", 12),
    ],
}

PAINTERS = {
    "wove": {k: (lambda kind: (lambda frame, k=kind: paint_wove(k, frame)))(k) for k in WOVES},
    "guilloche": {k: (lambda kind: (lambda frame, k=kind: paint_guilloche(k, frame)))(k) for k in GUILLOCHES},
    "bust": {k: (lambda kind: (lambda frame, k=kind: paint_bust(k, frame)))(k) for k in BUSTS},
    "surcharge": {k: (lambda kind: (lambda frame, k=kind: paint_surcharge(k, frame)))(k) for k in SURCHARGES},
    "aspect": {k: (lambda kind: (lambda frame, k=kind: paint_aspect(k, frame)))(k) for k in ASPECTS},
    "device": {k: (lambda kind: (lambda frame, k=kind: paint_device(k, frame)))(k) for k in DEVICES},
    "cancel": {k: (lambda kind: (lambda frame, k=kind: paint_cancel(k, frame)))(k) for k in CANCELS},
}

STACK = ("wove", "guilloche", "bust", "surcharge", "aspect", "device", "cancel")

SIGNATURES = [
    {"wove": "ivory", "guilloche": "rose", "bust": "pilot", "surcharge": "none", "aspect": "calm", "device": "goggles", "cancel": "cds"},
    {"wove": "buff", "guilloche": "tablet", "bust": "keeper", "surcharge": "bar", "aspect": "stern", "device": "pipe", "cancel": "waves"},
    {"wove": "azure", "guilloche": "engine", "bust": "captain", "surcharge": "band", "aspect": "glance", "device": "medal", "cancel": "bars"},
    {"wove": "sage", "guilloche": "sunburst", "bust": "botanist", "surcharge": "none", "aspect": "smile", "device": "none", "cancel": "none"},
    {"wove": "lilac", "guilloche": "lattice", "bust": "clerk", "surcharge": "oval", "aspect": "wink", "device": "specs", "cancel": "cds"},
    {"wove": "rose", "guilloche": "wave", "bust": "warden", "surcharge": "triangle", "aspect": "shout", "device": "cockade", "cancel": "mute"},
    {"wove": "pearl", "guilloche": "rose", "bust": "mapper", "surcharge": "none", "aspect": "stern", "device": "none", "cancel": "waves"},
    {"wove": "grey", "guilloche": "engine", "bust": "signal", "surcharge": "bar", "aspect": "calm", "device": "medal", "cancel": "cds"},
    {"wove": "ivory", "guilloche": "tablet", "bust": "captain", "surcharge": "oval", "aspect": "smile", "device": "goggles", "cancel": "none"},
    {"wove": "buff", "guilloche": "sunburst", "bust": "pilot", "surcharge": "band", "aspect": "wink", "device": "none", "cancel": "bars"},
    {"wove": "azure", "guilloche": "lattice", "bust": "keeper", "surcharge": "none", "aspect": "glance", "device": "cockade", "cancel": "cds"},
    {"wove": "sage", "guilloche": "wave", "bust": "clerk", "surcharge": "triangle", "aspect": "calm", "device": "pipe", "cancel": "mute"},
    {"wove": "lilac", "guilloche": "rose", "bust": "botanist", "surcharge": "bar", "aspect": "shout", "device": "specs", "cancel": "waves"},
    {"wove": "rose", "guilloche": "engine", "bust": "mapper", "surcharge": "none", "aspect": "smile", "device": "medal", "cancel": "cds"},
    {"wove": "pearl", "guilloche": "tablet", "bust": "warden", "surcharge": "band", "aspect": "stern", "device": "none", "cancel": "bars"},
    {"wove": "grey", "guilloche": "sunburst", "bust": "signal", "surcharge": "oval", "aspect": "wink", "device": "goggles", "cancel": "none"},
]

TRAIT_LABELS = (
    ("wove", "Wove"),
    ("guilloche", "Guilloche"),
    ("bust", "Bust"),
    ("surcharge", "Surcharge"),
    ("aspect", "Aspect"),
    ("device", "Device"),
    ("cancel", "Cancel"),
)

COLLECTION_DESCRIPTION = (
    "Perfin is an 8,888-piece collection of looping engraved postage-stamp PFP GIFs. "
    "Each frank is stacked from seven plates — wove, guilloche, bust, surcharge, aspect, device, and cancel — "
    "then flattened onto one 12-frame GIF. Intaglio hatch. Perforated edges. A cancellation that walks."
)

COLLECTION_STORY = (
    "Perfin.\n\n"
    "An 8,888-piece collection of looping engraved postage-stamp PFP GIFs on Robinhood Chain. "
    "Each frank is stacked from seven plates — wove, guilloche, bust, surcharge, aspect, device, and cancel — "
    "then flattened onto one 12-frame GIF. Eight busts, each its own stamp ink: pilot, keeper, clerk, captain, "
    "botanist, mapper, signal, and warden. Guilloche turns behind the vignette. A cancellation walks the face.\n\n"
    "Intaglio lines on wove paper. Perforated rectangle. No charcoal outline. No sticker cutout. "
    "No dancing blot. The bust stays seated. One shared clock.\n\n"
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
        "name": "Perfin",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Eight engraved busts share one vignette; devices and cancels never edit the bust file.",
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
                "name": f"Perfin #{index}",
                "image": f"/perfin-preview/{index}.gif",
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
    (SRC_DATA / "perfin-gallery.ts").write_text(
        "export type PerfinSample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const perfinSamples: PerfinSample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def write_ts_traits() -> None:
    blurbs = {
        "wove": "Stamp paper — ivory, rose, azure, buff, lilac, sage, pearl, grey.",
        "guilloche": "Security engraving behind the vignette — rose, engine, lattice, sunburst, wave, tablet.",
        "bust": "The franked portrait. Eight engraved busts: pilot, keeper, clerk, captain, botanist, mapper, signal, warden.",
        "surcharge": "A second ink overprint — carmine bar, Prussian band, orange triangle, violet oval — or none.",
        "aspect": "The face cut — calm, stern, wink, shout, glance, smile.",
        "device": "An engraved extra on the crown or chest — goggles, spectacles, medal, pipe, cockade — or a bare device.",
        "cancel": "The killer that walks — circular date, wavy lines, mute, bars — or mint uncancelled.",
    }
    none_labels = {
        "surcharge": "No Surcharge",
        "device": "Bare Device",
        "cancel": "Mint Uncancelled",
    }
    cats = []
    for key, label in TRAIT_LABELS:
        traits = []
        for trait_id, name, rarity in TRAIT_SPEC[key]:
            if trait_id == "none":
                continue
            traits.append(
                "      { "
                f'id: "{trait_id}", name: "{name}", image: "/perfin-traits/{key}/{trait_id}.png", rarity: {rarity} '
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
    (SRC_DATA / "perfin-traits.ts").write_text(
        "export type PerfinTrait = {\n"
        "  id: string;\n"
        "  name: string;\n"
        "  image?: string;\n"
        "  rarity: number;\n"
        "};\n\n"
        "export type PerfinTraitCategory = {\n"
        f"  id: {ids};\n"
        "  label: string;\n"
        "  blurb: string;\n"
        "  noneLabel?: string;\n"
        "  traits: PerfinTrait[];\n"
        "};\n\n"
        "/** Bump when APNG layers change so the studio does not keep a stale loop. */\n"
        'export const PERFIN_ART_VERSION = "perfin-v1";\n\n'
        "export const PERFIN_FRAMES = 12;\n"
        "export const PERFIN_DURATION_MS = 90;\n\n"
        "export function perfinTraitSrc(path?: string) {\n"
        "  if (!path) return \"\";\n"
        "  return `${path}?v=${PERFIN_ART_VERSION}`;\n"
        "}\n\n"
        "export const perfinTraitCategories: PerfinTraitCategory[] = [\n"
        + ",\n".join(cats)
        + "\n];\n\n"
        'export const nonePerfinTrait: PerfinTrait = { id: "none", name: "None", rarity: 0 };\n\n'
        "export function perfinCategoryById(id: PerfinTraitCategory[\"id\"]) {\n"
        "  const category = perfinTraitCategories.find((item) => item.id === id);\n"
        "  if (!category) throw new Error(`Unknown Perfin trait category: ${id}`);\n"
        "  return category;\n"
        "}\n\n"
        "export function findPerfinTrait(categoryId: PerfinTraitCategory[\"id\"], traitId: string) {\n"
        "  if (traitId === \"none\") return nonePerfinTrait;\n"
        "  return perfinCategoryById(categoryId).traits.find((trait) => trait.id === traitId);\n"
        "}\n\n"
        "export const defaultPerfinSelection = {\n"
        '  wove: "ivory",\n'
        '  guilloche: "rose",\n'
        '  bust: "pilot",\n'
        '  surcharge: "none",\n'
        '  aspect: "calm",\n'
        '  device: "goggles",\n'
        '  cancel: "cds",\n'
        "} as const;\n\n"
        "export type PerfinSelection = Record<PerfinTraitCategory[\"id\"], string>;\n\n"
        "export function randomPerfinSelection(): PerfinSelection {\n"
        "  const pick = (category: PerfinTraitCategory) => {\n"
        "    const pool: PerfinTrait[] = category.noneLabel\n"
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
        '    wove: pick(perfinCategoryById("wove")),\n'
        '    guilloche: pick(perfinCategoryById("guilloche")),\n'
        '    bust: pick(perfinCategoryById("bust")),\n'
        '    surcharge: pick(perfinCategoryById("surcharge")),\n'
        '    aspect: pick(perfinCategoryById("aspect")),\n'
        '    device: pick(perfinCategoryById("device")),\n'
        '    cancel: pick(perfinCategoryById("cancel")),\n'
        "  };\n"
        "}\n\n"
        "export function perfinCombinationCount() {\n"
        "  return perfinTraitCategories.reduce((product, category) => {\n"
        "    const extra = category.noneLabel ? 1 : 0;\n"
        "    return product * (category.traits.length + extra);\n"
        "  }, 1);\n"
        "}\n\n"
        "export function perfinSelectionToLayers(selection: PerfinSelection) {\n"
        '  return (["wove", "guilloche", "bust", "surcharge", "aspect", "device", "cancel"] as const)\n'
        "    .map((id) => findPerfinTrait(id, selection[id]))\n"
        "    .filter((trait): trait is PerfinTrait => Boolean(trait?.image))\n"
        "    .map((trait) => perfinTraitSrc(trait.image));\n"
        "}\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array(
        [
            [0.95, 0.93, 0.86],
            [0.61, 0.14, 0.21],
            [0.11, 0.21, 0.36],
            [0.91, 0.84, 0.73],
        ],
        dtype=np.float32,
    )
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)
    yy = np.linspace(0.0, 1.0, height, dtype=np.float32)[:, None]
    xx = np.broadcast_to(x, (height, width))
    t = np.clip(xx * 0.6 + yy * 0.4, 0.0, 0.999) * (len(colors) - 1)
    i0 = np.floor(t).astype(np.int32)
    f = (t - i0)[..., None]
    rgb_out = colors[i0] * (1.0 - f) + colors[np.clip(i0 + 1, 0, len(colors) - 1)] * f
    arr = np.dstack([np.clip(rgb_out * 255.0, 0, 255).astype(np.uint8), np.full((height, width), 255, dtype=np.uint8)])
    return Image.fromarray(arr, "RGBA")


def write_collection_meta() -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    (META_DIR / "perfin-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "perfin.json").write_text(
        json.dumps(
            {
                "name": "Perfin",
                "symbol": "PRFN",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-perfin.gif",
                "featured_image": "/brand/featured-perfin.jpg",
                "banner_image": "/brand/banner-perfin.png",
                "opensea_banner_image": "/brand/banner-perfin-opensea.jpg",
                "external_link": "/perfin",
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
        (12, 12, SIZE - 13, SIZE - 13), radius=40, outline=(155, 36, 54, 255), width=4
    )
    logo = Image.alpha_composite(logo, rim)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-perfin.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-perfin-loop.png",
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

    save_image(lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-perfin.png", quality=94)
    save_image(lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-perfin-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=28)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=28)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-perfin.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(
        gif_frames,
        BRAND_DIR / "collection-perfin.gif",
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
        print("Writing Perfin brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Perfin engraved stamps…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
