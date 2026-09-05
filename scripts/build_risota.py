#!/usr/bin/env python3
"""Paint Risota — dancing characters as overlapping risograph ink plates.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
The dancer stays seated on one envelope: head, shoulders, and hips share
a bounce so later plates can overprint. The second ink pass slides out
of register. That misregister is the motion signature.

Look: full-body dancers built from fat ink blots on uncoated paper.
Spot color. Soy-ink soak. Halftone mesh. No charcoal contour. No sticker
cutout. No egg torso. No notehead. No stick limb.
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

GIF_COLORS = 96
GIF_DITHER = Image.Dither.NONE

TRAIT_DIR = ROOT / "public" / "risota-traits"
PREVIEW_DIR = ROOT / "public" / "risota-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

STOCKS = ("cream", "blush", "mint", "kraft", "ice", "lemon", "fog", "recyc")
SCREENS = ("none", "rosa", "aqua", "gild", "navy", "ember")
FIGURES = ("kick", "twirl", "pop", "sway", "hop", "glide", "stomp", "reach")
PASSES = ("none", "smock", "bib", "sash", "cuff", "flare", "wrap")
KNOCKOUTS = ("dots", "grin", "wink", "shout", "focus", "calm")
SLUGS = ("none", "kerchief", "bow", "burst", "brim")
MARKS = ("none", "ticks", "splash", "stars", "crop")

# Classic risograph spot inks. Not a house palette.
INK = {
    "pink": (255, 48, 168),
    "teal": (0, 148, 148),
    "yellow": (255, 220, 0),
    "blue": (20, 56, 168),
    "red": (232, 40, 28),
    "green": (0, 120, 72),
    "gold": (196, 148, 48),
    "violet": (132, 48, 168),
    "wine": (52, 30, 38),
}

PAPER = {
    "cream": (248, 240, 220),
    "blush": (244, 214, 210),
    "mint": (214, 232, 218),
    "kraft": (198, 166, 118),
    "ice": (220, 228, 234),
    "lemon": (246, 236, 176),
    "fog": (228, 224, 218),
    "recyc": (208, 200, 184),
}

FIGURE_INK = {
    "kick": "pink",
    "twirl": "teal",
    "pop": "yellow",
    "sway": "blue",
    "hop": "red",
    "glide": "green",
    "stomp": "gold",
    "reach": "violet",
}

PASS_INK = {
    "smock": "teal",
    "bib": "yellow",
    "sash": "gold",
    "cuff": "blue",
    "flare": "red",
    "wrap": "pink",
}

SLUG_INK = {
    "kerchief": "yellow",
    "bow": "pink",
    "burst": "teal",
    "brim": "blue",
}

SCREEN_INK = {
    "rosa": "pink",
    "aqua": "teal",
    "gild": "gold",
    "navy": "blue",
    "ember": "red",
}


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def clock(frame: int) -> float:
    return frame / FRAMES * math.tau


def seed_for(*parts: object) -> int:
    payload = "|".join(map(str, parts)).encode()
    return int(hashlib.md5(payload).hexdigest()[:8], 16)


def rotate(x: float, y: float, cx: float, cy: float, ang: float) -> tuple[float, float]:
    s, c = math.sin(ang), math.cos(ang)
    dx, dy = x - cx, y - cy
    return cx + dx * c - dy * s, cy + dx * s + dy * c


def seat(frame: int) -> tuple[float, float, float]:
    """Shared dance envelope. Head / shoulder / hip stay locked for overprints."""
    t = clock(frame)
    sway = math.sin(t) * 7.0
    bounce = -12.0 * abs(math.sin(t * 2.0))
    lean = math.sin(t) * 0.11
    return sway, bounce, lean


def misregister(frame: int) -> tuple[float, float]:
    t = clock(frame)
    return math.sin(t * 1.35) * 8.0, math.cos(t * 1.1) * 5.0


def placed(
    x: float, y: float, sway: float, bounce: float, lean: float, hip: tuple[float, float]
) -> tuple[float, float]:
    x, y = rotate(x, y, hip[0], hip[1], lean)
    return x + sway, y + bounce


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


def ImageChops_lighter(a: Image.Image, b: Image.Image) -> Image.Image:
    return Image.fromarray(np.maximum(np.asarray(a), np.asarray(b)), "L")


def capsule_mask(x0: float, y0: float, x1: float, y1: float, radius: float) -> np.ndarray:
    layer = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(layer)
    width = max(2, int(round(radius * 2)))
    draw.line([(x0, y0), (x1, y1)], fill=255, width=width)
    draw.ellipse((x0 - radius, y0 - radius, x0 + radius, y0 + radius), fill=255)
    draw.ellipse((x1 - radius, y1 - radius, x1 + radius, y1 + radius), fill=255)
    return np.asarray(layer, dtype=np.uint8)


def poly_mask(points: list[tuple[float, float]]) -> np.ndarray:
    layer = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(layer).polygon([(int(round(x)), int(round(y))) for x, y in points], fill=255)
    return np.asarray(layer, dtype=np.uint8)


def ink_plate(
    mask: np.ndarray,
    rgb: tuple[int, int, int],
    opacity: float = 0.88,
    soak: float = 1.35,
    grain: float = 0.07,
    seed: int = 1,
) -> Image.Image:
    """One translucent spot-color plate. Soft soak at the edge. No contour."""
    if soak > 0:
        blurred = Image.fromarray(mask, "L").filter(ImageFilter.GaussianBlur(radius=soak))
        mask = np.asarray(blurred, dtype=np.uint8)
    rng = np.random.RandomState(seed)
    noise = rng.randn(SIZE, SIZE).astype(np.float32) * grain
    alpha = np.clip(mask.astype(np.float32) / 255.0 * opacity * (1.0 + noise), 0.0, 1.0)
    out = np.zeros((SIZE, SIZE, 4), dtype=np.uint8)
    out[..., 0] = rgb[0]
    out[..., 1] = rgb[1]
    out[..., 2] = rgb[2]
    out[..., 3] = (alpha * 255.0).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def paper_stock(kind: str, frame: int) -> Image.Image:
    base = np.array(PAPER[kind], dtype=np.float32)
    rng = np.random.RandomState(seed_for("stock", kind))
    tooth = rng.randn(SIZE, SIZE).astype(np.float32) * 5.0
    # Slow fiber drift so the sheet feels printed, not a still scan.
    t = clock(frame)
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    drift = 3.2 * np.sin(xx * 0.035 + t) + 2.4 * np.cos(yy * 0.028 - t * 0.7)
    rgb = np.clip(base + tooth[..., None] + drift[..., None], 0, 255).astype(np.uint8)
    out = np.dstack([rgb, np.full((SIZE, SIZE), 255, dtype=np.uint8)])
    return Image.fromarray(out, "RGBA")


def paint_stock(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    return paper_stock(kind, frame)


def paint_screen(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    rgb = INK[SCREEN_INK[kind]]
    t = clock(frame)
    mask = empty_mask()
    layer = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(layer)
    spacing = 11 if kind in ("rosa", "aqua") else 13
    phase_x = int(round(math.sin(t) * 3))
    phase_y = int(round(math.cos(t * 0.8) * 3))
    radius = 2 if kind != "gild" else 3
    for y in range(18 + phase_y, SIZE - 12, spacing):
        row_shift = (y // spacing) % 2 * (spacing // 2)
        for x in range(16 + phase_x + row_shift, SIZE - 12, spacing):
            wobble = 1 if ((x + y) // spacing) % 5 == 0 else 0
            draw.ellipse((x - radius - wobble, y - radius, x + radius + wobble, y + radius), fill=210)
    if kind == "gild":
        wash = Image.new("L", (SIZE, SIZE), 0)
        ImageDraw.Draw(wash).ellipse((40, 30, 480, 490), fill=48)
        wash = wash.filter(ImageFilter.GaussianBlur(radius=28))
        layer = ImageChops_lighter(layer, wash)
    if kind == "ember":
        for i in range(28):
            rng = np.random.RandomState(seed_for("ember", i))
            px = int(rng.randint(30, 480) + math.sin(t + i) * 6)
            py = int(rng.randint(30, 480) + math.cos(t * 0.9 + i) * 6)
            r = int(rng.randint(2, 5))
            draw.ellipse((px - r, py - r, px + r, py + r), fill=180)
    mask = np.asarray(layer, dtype=np.uint8)
    return ink_plate(mask, rgb, opacity=0.34, soak=0.8, grain=0.04, seed=seed_for("screen", kind))


def dancer_joints(kind: str, frame: int) -> dict[str, tuple[float, float]]:
    sway, bounce, lean = seat(frame)
    t = clock(frame)
    hip0 = (256.0, 318.0)
    shoulder0 = (256.0, 208.0)
    head0 = (256.0, 138.0)

    if kind == "hop":
        shoulder0 = (256.0, 222.0)
        head0 = (256.0, 154.0)
    elif kind == "reach":
        shoulder0 = (256.0, 188.0)
        head0 = (256.0, 118.0)
    elif kind == "glide":
        hip0 = (268.0, 322.0)
        shoulder0 = (248.0, 206.0)
        head0 = (236.0, 136.0)
    elif kind == "stomp":
        hip0 = (256.0, 324.0)
        shoulder0 = (256.0, 214.0)

    hip = (hip0[0] + sway, hip0[1] + bounce)
    shoulder = placed(*shoulder0, sway, bounce, lean, hip0)
    head = placed(*head0, sway, bounce, lean, hip0)
    sh_w = 38.0 if kind in ("pop", "stomp") else 32.0 if kind != "reach" else 26.0
    hp_w = 36.0 if kind in ("stomp", "twirl") else 24.0 if kind == "reach" else 28.0
    sh_l = placed(shoulder0[0] - sh_w, shoulder0[1] + 6, sway, bounce, lean, hip0)
    sh_r = placed(shoulder0[0] + sh_w, shoulder0[1] + 6, sway, bounce, lean, hip0)
    hp_l = placed(hip0[0] - hp_w, hip0[1] + 2, sway, bounce, lean, hip0)
    hp_r = placed(hip0[0] + hp_w, hip0[1] + 2, sway, bounce, lean, hip0)

    beat = 0.5 + 0.5 * math.sin(t)
    kick_up = max(0.0, math.sin(t))
    hop = abs(math.sin(t * 2.0))

    if kind == "kick":
        la1, la2 = -0.85, -0.55
        ra1, ra2 = 0.55 + 0.35 * beat, 0.85
        ll1, ll2 = -0.12, 0.08
        rl1, rl2 = 0.35 + 1.15 * kick_up, 0.55 + 0.55 * kick_up
    elif kind == "twirl":
        spin = t * 0.35
        la1, la2 = -1.15 + math.sin(spin) * 0.4, -1.6
        ra1, ra2 = 1.15 + math.cos(spin) * 0.4, 1.6
        ll1, ll2 = -0.28, 0.05
        rl1, rl2 = 0.28, -0.05
    elif kind == "pop":
        la1, la2 = -0.15, 0.05
        ra1, ra2 = 2.85, 3.15
        ll1, ll2 = -0.55, -0.15
        rl1, rl2 = 0.55, 0.15
    elif kind == "sway":
        la1, la2 = -2.5 - 0.2 * beat, -2.85
        ra1, ra2 = 0.7, 1.05
        ll1, ll2 = -0.22 - 0.12 * math.sin(t), 0.1
        rl1, rl2 = 0.18 + 0.12 * math.sin(t), 0.05
    elif kind == "hop":
        la1, la2 = -2.2, -2.55
        ra1, ra2 = 2.2, 2.55
        ll1, ll2 = -0.55 - 0.25 * hop, -0.85
        rl1, rl2 = 0.55 + 0.25 * hop, 0.85
    elif kind == "glide":
        la1, la2 = -1.7, -2.05
        ra1, ra2 = 1.35, 1.7
        ll1, ll2 = -0.85, -0.35
        rl1, rl2 = 0.15, 0.55
    elif kind == "stomp":
        la1, la2 = -0.45, -0.15
        ra1, ra2 = 0.45, 0.15
        ll1, ll2 = -0.72, -0.2
        rl1, rl2 = 0.72, 0.2
    else:  # reach
        la1, la2 = -2.95, -3.12
        ra1, ra2 = 2.95, 3.12
        ll1, ll2 = -0.1, 0.05
        rl1, rl2 = 0.1, -0.05

    def extend(origin: tuple[float, float], ang: float, length: float) -> tuple[float, float]:
        return origin[0] + length * math.sin(ang), origin[1] + length * math.cos(ang)

    arm_u, arm_l = (68.0, 62.0) if kind != "reach" else (78.0, 70.0)
    leg_u, leg_l = (86.0, 82.0) if kind != "hop" else (70.0, 62.0)
    if kind == "glide":
        leg_u, leg_l = 92.0, 88.0

    l_elbow = extend(sh_l, la1, arm_u)
    l_hand = extend(l_elbow, la2, arm_l)
    r_elbow = extend(sh_r, ra1, arm_u)
    r_hand = extend(r_elbow, ra2, arm_l)
    l_knee = extend(hp_l, ll1, leg_u)
    l_foot = extend(l_knee, ll2, leg_l)
    r_knee = extend(hp_r, rl1, leg_u)
    r_foot = extend(r_knee, rl2, leg_l)

    return {
        "hip": hip,
        "shoulder": shoulder,
        "head": head,
        "sh_l": sh_l,
        "sh_r": sh_r,
        "hp_l": hp_l,
        "hp_r": hp_r,
        "l_elbow": l_elbow,
        "l_hand": l_hand,
        "r_elbow": r_elbow,
        "r_hand": r_hand,
        "l_knee": l_knee,
        "l_foot": l_foot,
        "r_knee": r_knee,
        "r_foot": r_foot,
    }


def figure_mask(kind: str, frame: int) -> np.ndarray:
    j = dancer_joints(kind, frame)
    mask = empty_mask()
    torso_w = {
        "kick": 58.0,
        "twirl": 50.0,
        "pop": 70.0,
        "sway": 46.0,
        "hop": 64.0,
        "glide": 44.0,
        "stomp": 74.0,
        "reach": 40.0,
    }[kind]
    torso_h = 78.0 if kind != "hop" else 64.0
    cx = (j["shoulder"][0] + j["hip"][0]) / 2
    cy = (j["shoulder"][1] + j["hip"][1]) / 2
    lean = math.atan2(j["shoulder"][0] - j["hip"][0], j["hip"][1] - j["shoulder"][1])
    mask = or_mask(mask, ellipse_mask(cx, cy, torso_w, torso_h, lean))
    # Pelvis blot — hips have mass, this is not an egg.
    mask = or_mask(mask, ellipse_mask(j["hip"][0], j["hip"][1] + 6, torso_w * 0.92, 34.0, lean * 0.4))
    # Chest blot
    mask = or_mask(mask, ellipse_mask(j["shoulder"][0], j["shoulder"][1] + 10, torso_w * 0.88, 32.0, lean))

    arm_r = 16.0 if kind != "reach" else 13.0
    leg_r = 19.0 if kind not in ("reach", "glide") else 15.0
    if kind == "stomp":
        arm_r, leg_r = 18.0, 22.0
    mask = or_mask(mask, capsule_mask(*j["sh_l"], *j["l_elbow"], arm_r))
    mask = or_mask(mask, capsule_mask(*j["l_elbow"], *j["l_hand"], arm_r * 0.9))
    mask = or_mask(mask, capsule_mask(*j["sh_r"], *j["r_elbow"], arm_r))
    mask = or_mask(mask, capsule_mask(*j["r_elbow"], *j["r_hand"], arm_r * 0.9))
    mask = or_mask(mask, capsule_mask(*j["hp_l"], *j["l_knee"], leg_r))
    mask = or_mask(mask, capsule_mask(*j["l_knee"], *j["l_foot"], leg_r * 0.92))
    mask = or_mask(mask, capsule_mask(*j["hp_r"], *j["r_knee"], leg_r))
    mask = or_mask(mask, capsule_mask(*j["r_knee"], *j["r_foot"], leg_r * 0.92))

    # Mitten hands and wedge feet — volume, not sticks.
    mask = or_mask(mask, ellipse_mask(j["l_hand"][0], j["l_hand"][1], 15, 13))
    mask = or_mask(mask, ellipse_mask(j["r_hand"][0], j["r_hand"][1], 15, 13))
    mask = or_mask(mask, ellipse_mask(j["l_foot"][0] + 6, j["l_foot"][1] + 4, 22, 11, 0.15))
    mask = or_mask(mask, ellipse_mask(j["r_foot"][0] - 6, j["r_foot"][1] + 4, 22, 11, -0.15))

    hx, hy = j["head"]
    # Irregular head: two offset blots, not a sticker circle.
    mask = or_mask(mask, ellipse_mask(hx - 3, hy - 2, 36, 40, -0.12))
    mask = or_mask(mask, ellipse_mask(hx + 8, hy + 4, 28, 30, 0.2))
    mask = or_mask(mask, capsule_mask(hx, hy + 28, j["shoulder"][0], j["shoulder"][1] - 4, 12))

    if kind == "twirl":
        flare = 88.0 + 18.0 * abs(math.sin(clock(frame)))
        mask = or_mask(mask, ellipse_mask(j["hip"][0], j["hip"][1] + 18, flare, 38.0, lean * 0.5))
    if kind == "sway":
        mask = or_mask(mask, ellipse_mask(j["hip"][0] + 10, j["hip"][1] + 8, 62, 30, 0.35))
    if kind == "pop":
        mask = or_mask(mask, ellipse_mask(j["l_hand"][0], j["l_hand"][1] + 8, 18, 10))

    # Ground blot — a printed puddle, not a drop shadow.
    gx = (j["l_foot"][0] + j["r_foot"][0]) / 2
    gy = max(j["l_foot"][1], j["r_foot"][1]) + 10
    mask = or_mask(mask, ellipse_mask(gx, gy, 54, 10))
    return mask


def paint_figure(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    rgb = INK[FIGURE_INK[kind]]
    return ink_plate(
        figure_mask(kind, frame),
        rgb,
        opacity=0.90,
        soak=1.5,
        grain=0.06,
        seed=seed_for("figure", kind, frame // 3),
    )


def pass_mask(kind: str, frame: int, figure: str = "kick") -> np.ndarray:
    j = dancer_joints(figure, frame)
    dx, dy = misregister(frame)
    def sh(pt: tuple[float, float]) -> tuple[float, float]:
        return pt[0] + dx, pt[1] + dy

    hip, shoulder, head = sh(j["hip"]), sh(j["shoulder"]), sh(j["head"])
    mask = empty_mask()
    if kind == "smock":
        mask = or_mask(mask, ellipse_mask((shoulder[0] + hip[0]) / 2, (shoulder[1] + hip[1]) / 2 + 8, 72, 92))
        mask = or_mask(mask, ellipse_mask(hip[0], hip[1] + 28, 80, 40))
    elif kind == "bib":
        mask = or_mask(
            mask,
            poly_mask(
                [
                    (shoulder[0] - 40, shoulder[1] - 4),
                    (shoulder[0] + 40, shoulder[1] - 4),
                    (hip[0] + 28, hip[1] + 8),
                    (hip[0] - 28, hip[1] + 8),
                ]
            ),
        )
    elif kind == "sash":
        mask = or_mask(
            mask,
            poly_mask(
                [
                    (shoulder[0] - 62, shoulder[1] - 18),
                    (shoulder[0] - 28, shoulder[1] - 30),
                    (hip[0] + 58, hip[1] + 36),
                    (hip[0] + 22, hip[1] + 50),
                ]
            ),
        )
    elif kind == "cuff":
        mask = or_mask(mask, capsule_mask(*sh(j["l_knee"]), *sh(j["l_foot"]), 22))
        mask = or_mask(mask, capsule_mask(*sh(j["r_knee"]), *sh(j["r_foot"]), 22))
    elif kind == "flare":
        mask = or_mask(mask, ellipse_mask(hip[0], hip[1] + 22, 96 + 10 * abs(math.sin(clock(frame))), 42))
    elif kind == "wrap":
        mask = or_mask(mask, ellipse_mask(hip[0], hip[1] - 4, 78, 22, 0.08))
    return mask


def paint_pass(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    # Pass art is seated on the shared envelope (kick seating) so every figure
    # overprints the same torso clock. The plate itself is the clothing blot.
    rgb = INK[PASS_INK[kind]]
    return ink_plate(
        pass_mask(kind, frame, "kick"),
        rgb,
        opacity=0.58,
        soak=1.6,
        grain=0.05,
        seed=seed_for("pass", kind),
    )


def paint_knockout(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    j = dancer_joints("kick", frame)
    hx, hy = j["head"]
    t = clock(frame)
    blink = 1.0 if frame % 12 not in (3, 4) else 0.28
    mask = empty_mask()
    if kind in ("dots", "grin", "shout", "focus"):
        rx = 8.5 if kind != "focus" else 6.5
        gap = 15 if kind != "focus" else 11
        mask = or_mask(mask, ellipse_mask(hx - gap, hy - 4, rx, rx * blink + 2.0))
        mask = or_mask(mask, ellipse_mask(hx + gap, hy - 4, rx, rx * blink + 2.0))
    if kind == "wink":
        mask = or_mask(mask, ellipse_mask(hx - 15, hy - 4, 8.5, 8.5 * blink + 1.6))
        mask = or_mask(mask, ellipse_mask(hx + 15, hy - 2, 10.0, 3.0))
    if kind == "calm":
        mask = or_mask(mask, ellipse_mask(hx - 15, hy - 2, 10.0, 3.2))
        mask = or_mask(mask, ellipse_mask(hx + 15, hy - 2, 10.0, 3.2))
    if kind == "grin":
        smile = Image.new("L", (SIZE, SIZE), 0)
        ImageDraw.Draw(smile).chord((hx - 20, hy + 8, hx + 20, hy + 34), 8, 172, fill=255)
        inner = Image.new("L", (SIZE, SIZE), 0)
        ImageDraw.Draw(inner).ellipse((hx - 14, hy + 8, hx + 14, hy + 24), fill=255)
        smile_arr = np.asarray(smile, dtype=np.int16) - np.asarray(inner, dtype=np.int16)
        mask = or_mask(mask, np.clip(smile_arr, 0, 255).astype(np.uint8))
    if kind == "shout":
        mask = or_mask(mask, ellipse_mask(hx, hy + 18, 10, 12 + 2 * abs(math.sin(t))))
    if kind == "dots":
        mask = or_mask(mask, ellipse_mask(hx, hy + 16, 4.5, 4.0))
    return ink_plate(mask, (28, 18, 24), opacity=0.94, soak=0.55, grain=0.02, seed=seed_for("knock", kind))


def paint_slug(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    j = dancer_joints("kick", frame)
    hx, hy = j["head"]
    dx, dy = misregister(frame)
    hx, hy = hx + dx * 0.45, hy + dy * 0.45
    mask = empty_mask()
    if kind == "kerchief":
        mask = or_mask(
            mask,
            poly_mask([(hx + 8, hy - 28), (hx + 48, hy - 8), (hx + 22, hy + 6), (hx + 4, hy - 6)]),
        )
        mask = or_mask(mask, ellipse_mask(hx + 10, hy - 16, 22, 14, 0.4))
    elif kind == "bow":
        neck = (j["shoulder"][0] + dx * 0.45, j["shoulder"][1] - 8 + dy * 0.45)
        mask = or_mask(mask, ellipse_mask(neck[0] - 16, neck[1], 16, 10, -0.4))
        mask = or_mask(mask, ellipse_mask(neck[0] + 16, neck[1], 16, 10, 0.4))
        mask = or_mask(mask, ellipse_mask(neck[0], neck[1], 7, 7))
    elif kind == "burst":
        for i, ang in enumerate(np.linspace(-2.4, -0.6, 5)):
            length = 34 + 6 * math.sin(clock(frame) + i)
            tx = hx + math.cos(ang) * length
            ty = hy - 8 + math.sin(ang) * length * 0.35 - 16
            mask = or_mask(mask, capsule_mask(hx, hy - 22, tx, ty, 8))
            mask = or_mask(mask, ellipse_mask(tx, ty, 11, 9))
    elif kind == "brim":
        mask = or_mask(mask, ellipse_mask(hx, hy - 26, 58, 12, 0.05))
        mask = or_mask(mask, ellipse_mask(hx, hy - 34, 28, 14))
    return ink_plate(mask, INK[SLUG_INK[kind]], opacity=0.72, soak=1.2, grain=0.04, seed=seed_for("slug", kind))


def paint_mark(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    t = clock(frame)
    pulse = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t * 2))
    mask = empty_mask()
    layer = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(layer)
    if kind == "ticks":
        for cx, cy in ((36, 36), (476, 36), (36, 476), (476, 476)):
            draw.rectangle((cx - 10, cy - 2, cx + 10, cy + 2), fill=255)
            draw.rectangle((cx - 2, cy - 10, cx + 2, cy + 10), fill=255)
    elif kind == "splash":
        rng = np.random.RandomState(seed_for("splash"))
        ox = 400 + math.sin(t) * 8
        oy = 96 + math.cos(t) * 6
        for i in range(14):
            ang = rng.random() * math.tau
            dist = rng.random() * 38
            r = rng.randint(4, 14)
            draw.ellipse(
                (ox + math.cos(ang) * dist - r, oy + math.sin(ang) * dist - r,
                 ox + math.cos(ang) * dist + r, oy + math.sin(ang) * dist + r),
                fill=220,
            )
    elif kind == "stars":
        for cx, cy, s in ((86, 92, 16), (430, 120, 12), (400, 400, 14), (70, 390, 10)):
            pts = []
            for i in range(8):
                rad = s if i % 2 == 0 else s * 0.38
                ang = i * math.pi / 4 + t * 0.2
                pts.append((cx + math.cos(ang) * rad, cy + math.sin(ang) * rad))
            ImageDraw.Draw(layer).polygon(pts, fill=255)
    elif kind == "crop":
        for cx, cy, sx, sy in ((28, 28, 1, 1), (462, 28, 1, 1), (28, 462, 1, 1), (462, 462, 1, 1)):
            draw.rectangle((cx, cy, cx + 22, cy + 4), fill=255)
            draw.rectangle((cx, cy, cx + 4, cy + 22), fill=255)
    mask = np.asarray(layer, dtype=np.uint8)
    color = INK["wine"] if kind in ("ticks", "crop") else INK["pink"] if kind == "stars" else INK["teal"]
    return ink_plate(mask, color, opacity=0.55 * pulse + 0.2, soak=0.5, grain=0.02, seed=seed_for("mark", kind))


TRAIT_SPEC: dict[str, list[tuple[str, str, int]]] = {
    "stock": [
        ("cream", "Cream Sheet", 18),
        ("blush", "Blush Sheet", 14),
        ("mint", "Mint Sheet", 12),
        ("kraft", "Kraft Sheet", 12),
        ("ice", "Ice Sheet", 12),
        ("lemon", "Lemon Sheet", 12),
        ("fog", "Fog Sheet", 10),
        ("recyc", "Recycled Sheet", 10),
    ],
    "screen": [
        ("none", "Bare Stock", 22),
        ("rosa", "Rosa Mesh", 18),
        ("aqua", "Aqua Mesh", 16),
        ("gild", "Gild Mist", 14),
        ("navy", "Navy Mesh", 12),
        ("ember", "Ember Dust", 10),
    ],
    "figure": [
        ("kick", "Kick", 18),
        ("twirl", "Twirl", 16),
        ("pop", "Pop", 14),
        ("sway", "Sway", 14),
        ("hop", "Hop", 12),
        ("glide", "Glide", 10),
        ("stomp", "Stomp", 8),
        ("reach", "Reach", 8),
    ],
    "pass": [
        ("none", "Open Plate", 22),
        ("smock", "Smock Pass", 16),
        ("bib", "Bib Pass", 14),
        ("sash", "Sash Pass", 14),
        ("cuff", "Cuff Pass", 12),
        ("flare", "Flare Pass", 12),
        ("wrap", "Wrap Pass", 10),
    ],
    "knockout": [
        ("dots", "Dots", 22),
        ("grin", "Grin", 18),
        ("wink", "Wink", 16),
        ("shout", "Shout", 16),
        ("focus", "Focus", 14),
        ("calm", "Calm", 14),
    ],
    "slug": [
        ("none", "Clear Slug", 28),
        ("kerchief", "Kerchief", 18),
        ("bow", "Bow", 16),
        ("burst", "Burst", 14),
        ("brim", "Brim", 12),
    ],
    "mark": [
        ("none", "Clean Grip", 28),
        ("ticks", "Reg Ticks", 18),
        ("splash", "Ink Splash", 16),
        ("stars", "Star Burst", 14),
        ("crop", "Crop Marks", 12),
    ],
}

PAINTERS = {
    "stock": {k: (lambda kind: (lambda frame, k=kind: paint_stock(k, frame)))(k) for k in STOCKS},
    "screen": {k: (lambda kind: (lambda frame, k=kind: paint_screen(k, frame)))(k) for k in SCREENS},
    "figure": {k: (lambda kind: (lambda frame, k=kind: paint_figure(k, frame)))(k) for k in FIGURES},
    "pass": {k: (lambda kind: (lambda frame, k=kind: paint_pass(k, frame)))(k) for k in PASSES},
    "knockout": {k: (lambda kind: (lambda frame, k=kind: paint_knockout(k, frame)))(k) for k in KNOCKOUTS},
    "slug": {k: (lambda kind: (lambda frame, k=kind: paint_slug(k, frame)))(k) for k in SLUGS},
    "mark": {k: (lambda kind: (lambda frame, k=kind: paint_mark(k, frame)))(k) for k in MARKS},
}

STACK = ("stock", "screen", "figure", "pass", "knockout", "slug", "mark")

SIGNATURES = [
    {"stock": "cream", "screen": "rosa", "figure": "kick", "pass": "smock", "knockout": "grin", "slug": "kerchief", "mark": "ticks"},
    {"stock": "kraft", "screen": "navy", "figure": "stomp", "pass": "smock", "knockout": "shout", "slug": "burst", "mark": "splash"},
    {"stock": "mint", "screen": "aqua", "figure": "twirl", "pass": "flare", "knockout": "wink", "slug": "bow", "mark": "stars"},
    {"stock": "ice", "screen": "gild", "figure": "glide", "pass": "wrap", "knockout": "calm", "slug": "brim", "mark": "none"},
    {"stock": "blush", "screen": "ember", "figure": "hop", "pass": "bib", "knockout": "dots", "slug": "none", "mark": "crop"},
    {"stock": "lemon", "screen": "rosa", "figure": "pop", "pass": "cuff", "knockout": "focus", "slug": "kerchief", "mark": "ticks"},
    {"stock": "fog", "screen": "none", "figure": "sway", "pass": "none", "knockout": "grin", "slug": "bow", "mark": "none"},
    {"stock": "recyc", "screen": "aqua", "figure": "reach", "pass": "sash", "knockout": "shout", "slug": "burst", "mark": "stars"},
    {"stock": "cream", "screen": "gild", "figure": "twirl", "pass": "smock", "knockout": "calm", "slug": "brim", "mark": "crop"},
    {"stock": "kraft", "screen": "ember", "figure": "kick", "pass": "flare", "knockout": "wink", "slug": "none", "mark": "splash"},
    {"stock": "mint", "screen": "navy", "figure": "stomp", "pass": "wrap", "knockout": "dots", "slug": "kerchief", "mark": "ticks"},
    {"stock": "ice", "screen": "rosa", "figure": "glide", "pass": "bib", "knockout": "focus", "slug": "bow", "mark": "none"},
    {"stock": "blush", "screen": "none", "figure": "hop", "pass": "none", "knockout": "shout", "slug": "burst", "mark": "stars"},
    {"stock": "lemon", "screen": "aqua", "figure": "pop", "pass": "sash", "knockout": "grin", "slug": "brim", "mark": "crop"},
    {"stock": "fog", "screen": "gild", "figure": "sway", "pass": "cuff", "knockout": "calm", "slug": "none", "mark": "splash"},
    {"stock": "recyc", "screen": "ember", "figure": "reach", "pass": "smock", "knockout": "wink", "slug": "kerchief", "mark": "ticks"},
]

TRAIT_LABELS = (
    ("stock", "Stock"),
    ("screen", "Screen"),
    ("figure", "Figure"),
    ("pass", "Pass"),
    ("knockout", "Knockout"),
    ("slug", "Slug"),
    ("mark", "Mark"),
)

COLLECTION_DESCRIPTION = (
    "Risota is an 8,888-piece collection of looping risograph PFP GIFs. "
    "Each print is stacked from seven plates — stock, screen, figure, pass, knockout, slug, and mark — "
    "then flattened onto one 12-frame GIF. Dancing characters as overlapping ink. Misregister on the beat."
)

COLLECTION_STORY = (
    "Risota.\n\n"
    "An 8,888-piece collection of looping risograph PFP GIFs on Robinhood Chain. "
    "Each print is stacked from seven plates — stock, screen, figure, pass, knockout, slug, and mark — "
    "then flattened onto one 12-frame GIF. Eight dancers, each its own spot ink: kick, twirl, pop, sway, "
    "hop, glide, stomp, and reach. A second plate slides out of register. Halftone hangs on the sheet. "
    "Faces knock through as a dark drum.\n\n"
    "Soy ink on uncoated paper. Fat blots, not outlines. No sticker edge. No egg body. "
    "The dancer stays seated on one envelope. One shared clock.\n\n"
    "Minting on Robinhood Chain (chain ID 4663). Gas is ETH."
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
        "name": "Risota",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Eight dancers share one envelope; passes and slugs never edit the figure file.",
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
                "name": f"Print #{index}",
                "image": f"/risota-preview/{index}.gif",
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
    (SRC_DATA / "risota-gallery.ts").write_text(
        "export type RisotaSample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const risotaSamples: RisotaSample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def write_ts_traits() -> None:
    blurbs = {
        "stock": "Uncoated paper — cream, blush, mint, kraft, ice, lemon, fog, recycled.",
        "screen": "Halftone hanging on the sheet — rosa, aqua, gild, navy, ember — or bare stock.",
        "figure": "The dancer. Eight spot-ink bodies: kick, twirl, pop, sway, hop, glide, stomp, reach.",
        "pass": "Second ink drum — smock, bib, sash, cuff, flare, wrap — sliding out of register.",
        "knockout": "Face plate punched as a dark drum — dots, grin, wink, shout, focus, calm.",
        "slug": "A third blot on the crown or throat — kerchief, bow, burst, brim — or a clear slug.",
        "mark": "Press ephemera — registration ticks, splash, stars, crop marks — or a clean gripper.",
    }
    none_labels = {
        "screen": "Bare Stock",
        "pass": "Open Plate",
        "slug": "Clear Slug",
        "mark": "Clean Grip",
    }
    cats = []
    for key, label in TRAIT_LABELS:
        traits = []
        for trait_id, name, rarity in TRAIT_SPEC[key]:
            if trait_id == "none":
                continue
            traits.append(
                "      { "
                f'id: "{trait_id}", name: "{name}", image: "/risota-traits/{key}/{trait_id}.png", rarity: {rarity} '
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
    (SRC_DATA / "risota-traits.ts").write_text(
        "export type RisotaTrait = {\n"
        "  id: string;\n"
        "  name: string;\n"
        "  image?: string;\n"
        "  rarity: number;\n"
        "};\n\n"
        "export type RisotaTraitCategory = {\n"
        f"  id: {ids};\n"
        "  label: string;\n"
        "  blurb: string;\n"
        "  noneLabel?: string;\n"
        "  traits: RisotaTrait[];\n"
        "};\n\n"
        "/** Bump when APNG layers change so the studio does not keep a stale loop. */\n"
        'export const RISOTA_ART_VERSION = "risota-v1";\n\n'
        "export const RISOTA_FRAMES = 12;\n"
        "export const RISOTA_DURATION_MS = 90;\n\n"
        "export function risotaTraitSrc(path?: string) {\n"
        "  if (!path) return \"\";\n"
        "  return `${path}?v=${RISOTA_ART_VERSION}`;\n"
        "}\n\n"
        "export const risotaTraitCategories: RisotaTraitCategory[] = [\n"
        + ",\n".join(cats)
        + "\n];\n\n"
        'export const noneRisotaTrait: RisotaTrait = { id: "none", name: "None", rarity: 0 };\n\n'
        "export function risotaCategoryById(id: RisotaTraitCategory[\"id\"]) {\n"
        "  const category = risotaTraitCategories.find((item) => item.id === id);\n"
        "  if (!category) throw new Error(`Unknown Risota trait category: ${id}`);\n"
        "  return category;\n"
        "}\n\n"
        "export function findRisotaTrait(categoryId: RisotaTraitCategory[\"id\"], traitId: string) {\n"
        "  if (traitId === \"none\") return noneRisotaTrait;\n"
        "  return risotaCategoryById(categoryId).traits.find((trait) => trait.id === traitId);\n"
        "}\n\n"
        "export const defaultRisotaSelection = {\n"
        '  stock: "cream",\n'
        '  screen: "rosa",\n'
        '  figure: "kick",\n'
        '  pass: "smock",\n'
        '  knockout: "grin",\n'
        '  slug: "kerchief",\n'
        '  mark: "ticks",\n'
        "} as const;\n\n"
        "export type RisotaSelection = Record<RisotaTraitCategory[\"id\"], string>;\n\n"
        "export function randomRisotaSelection(): RisotaSelection {\n"
        "  const pick = (category: RisotaTraitCategory) => {\n"
        "    const pool: RisotaTrait[] = category.noneLabel\n"
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
        '    stock: pick(risotaCategoryById("stock")),\n'
        '    screen: pick(risotaCategoryById("screen")),\n'
        '    figure: pick(risotaCategoryById("figure")),\n'
        '    pass: pick(risotaCategoryById("pass")),\n'
        '    knockout: pick(risotaCategoryById("knockout")),\n'
        '    slug: pick(risotaCategoryById("slug")),\n'
        '    mark: pick(risotaCategoryById("mark")),\n'
        "  };\n"
        "}\n\n"
        "export function risotaCombinationCount() {\n"
        "  return risotaTraitCategories.reduce((product, category) => {\n"
        "    const extra = category.noneLabel ? 1 : 0;\n"
        "    return product * (category.traits.length + extra);\n"
        "  }, 1);\n"
        "}\n\n"
        "export function risotaSelectionToLayers(selection: RisotaSelection) {\n"
        '  return (["stock", "screen", "figure", "pass", "knockout", "slug", "mark"] as const)\n'
        "    .map((id) => findRisotaTrait(id, selection[id]))\n"
        "    .filter((trait): trait is RisotaTrait => Boolean(trait?.image))\n"
        "    .map((trait) => risotaTraitSrc(trait.image));\n"
        "}\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array(
        [
            [0.97, 0.94, 0.86],
            [1.00, 0.19, 0.66],
            [0.00, 0.58, 0.58],
            [0.97, 0.86, 0.69],
        ],
        dtype=np.float32,
    )
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)
    y = np.linspace(0.0, 1.0, height, dtype=np.float32)
    xx, yy = np.mgrid[0:height, 0:width].astype(np.float32)
    xx = xx * 0 + x
    yy = (yy / max(height - 1, 1))
    t = np.clip(xx * 0.62 + yy * 0.38, 0.0, 0.999) * (len(colors) - 1)
    i0 = np.floor(t).astype(np.int32)
    f = (t - i0)[..., None]
    c0 = colors[i0]
    c1 = colors[np.clip(i0 + 1, 0, len(colors) - 1)]
    rgb_out = c0 * (1.0 - f) + c1 * f
    rng = np.random.RandomState(46638888)
    tooth = rng.randn(height, width).astype(np.float32) * 0.03
    rgb_out = np.clip(rgb_out + tooth[..., None], 0, 1)
    arr = np.dstack([np.clip(rgb_out * 255.0, 0, 255).astype(np.uint8), np.full((height, width), 255, dtype=np.uint8)])
    return Image.fromarray(arr, "RGBA")


def write_collection_meta() -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    (META_DIR / "risota-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "risota.json").write_text(
        json.dumps(
            {
                "name": "Risota",
                "symbol": "RISO",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-risota.gif",
                "featured_image": "/brand/featured-risota.jpg",
                "banner_image": "/brand/banner-risota.png",
                "opensea_banner_image": "/brand/banner-risota-opensea.jpg",
                "external_link": "/risota",
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
    ImageDraw.Draw(rim).rounded_rectangle(
        (12, 12, SIZE - 13, SIZE - 13), radius=52, outline=(255, 48, 168, 255), width=4
    )
    logo = Image.alpha_composite(logo, rim)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-risota.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-risota-loop.png",
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

    save_image(lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-risota.png", quality=94)
    save_image(lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-risota-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=48)
    place_portrait(featured, portraits[2], 540, 130, 560, radius=48)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-risota.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(
        gif_frames,
        BRAND_DIR / "collection-risota.gif",
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
        print("Writing Risota brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Risota risograph dancers…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
