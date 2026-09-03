#!/usr/bin/env python3
"""Paint Foxkins — Mix 3 three-quarter loaf-orb fox, layered like Shook'ums.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
Pelt, mug, hat, and wrap share one hover so accessories never warp the skeleton.
Field stays still. Charm floats on its own tiny bob.

Look: painted 3D clay — BAYC form-light with Doodles volume.
One plump loaf-orb. Croissant tail on the left. Face offset right.
Three pelts only: maple, snow, dusk. Hats sit between the ears.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_shookums import (  # noqa: E402
    DURATION_MS,
    FRAMES,
    H,
    LINE,
    SIZE,
    W,
    XX,
    YY,
    blank,
    blit_soft,
    blit_volume,
    bump_normals,
    clamp01,
    clip_disc,
    disc,
    ellipsoid,
    ellipse,
    fill_poly,
    grain,
    hover_y,
    lite,
    mix,
    outline_disk,
    over,
    outlined_ellipse,
    outlined_poly,
    place_portrait,
    rgb,
    save_apng,
    save_image,
    shade,
    to_image,
    volume_ball,
)
from gif_bake import save_loop_gif  # noqa: E402

TRAIT_DIR = ROOT / "public" / "foxkins-traits"
PREVIEW_DIR = ROOT / "public" / "foxkins-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

# Mix 3 locked skeleton — three-quarter loaf-orb, facing slightly right.
# Accessories must sit on these points. Never edit per trait.
CX, CY = 252.0, 304.0
RX, RY = 166.0, 158.0
HEAD_X, HEAD_Y = 280.0, 228.0
HAT_X, HAT_Y = 278.0, 118.0
WRAP_X, WRAP_Y = 272.0, 292.0
CHARM_X, CHARM_Y = 398.0, 352.0
LINE_W = 9.0

FIELDS = {
    "grove": rgb("3a5a3a"),
    "snow": rgb("d8e0e8"),
    "dusk": rgb("3a2a48"),
    "hearth": rgb("5a2e22"),
}

PELTS = {
    "maple": {"fur": rgb("e87a3a"), "cream": rgb("f8e2c4"), "ear": rgb("c45a48"), "pad": rgb("d6766c")},
    "snow": {"fur": rgb("ece4da"), "cream": rgb("fff8f0"), "ear": rgb("e8a898"), "pad": rgb("e28a82")},
    "dusk": {"fur": rgb("5c4870"), "cream": rgb("d6b8b0"), "ear": rgb("a85868"), "pad": rgb("8a4858")},
}

MUGS = ("blink", "grin", "sleepy", "spark", "wink", "pout", "heart", "blep")
HATS = ("none", "beret", "cap", "flower", "leaf", "beanie", "bow")
WRAPS = ("none", "scarf", "bandana", "bell")
CHARMS = ("none", "acorn", "leaf", "lantern")


def merge_volumes(parts: list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    out_a = np.zeros((H, W), dtype=np.float32)
    out_nx = np.zeros((H, W), dtype=np.float32)
    out_ny = np.zeros((H, W), dtype=np.float32)
    out_nz = np.zeros((H, W), dtype=np.float32)
    for pnx, pny, pnz, pa in parts:
        choose = pa >= out_a
        out_nx = np.where(choose, pnx, out_nx)
        out_ny = np.where(choose, pny, out_ny)
        out_nz = np.where(choose, pnz, out_nz)
        out_a = np.maximum(out_a, pa)
    return out_nx, out_ny, out_nz, out_a


def fox_volume(cx: float, cy: float, rx: float = RX, ry: float = RY) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """One locked Mix 3 silhouette: croissant tail, loaf-orb, 3/4 head, ears, tucked paws."""
    hx, hy = cx + 28.0, cy - 76.0
    parts = [
        ellipsoid(cx - rx * 0.92, cy + 18.0, 52.0, 44.0, soft=1.7),
        ellipsoid(cx - rx * 1.04, cy - 18.0, 44.0, 40.0, soft=1.7),
        ellipsoid(cx - rx * 0.86, cy - 58.0, 36.0, 34.0, soft=1.8),
        ellipsoid(cx, cy, rx, ry, soft=1.55),
        ellipsoid(hx, hy, 108.0, 100.0, soft=1.5),
        ellipsoid(hx - 22.0, hy + 18.0, 38.0, 28.0, soft=1.8),
        ellipsoid(hx + 36.0, hy + 14.0, 42.0, 30.0, soft=1.8),
        ellipsoid(cx - 46.0, cy + ry * 0.70, 30.0, 22.0, soft=1.7),
        ellipsoid(cx + 46.0, cy + ry * 0.74, 32.0, 22.0, soft=1.7),
    ]
    return merge_volumes(parts)


def blink_amount(frame: int) -> float:
    if frame in (5, 6):
        return 1.0
    if frame == 4:
        return 0.55
    if frame == 7:
        return 0.35
    return 0.0


def paint_field(kind: str, _frame: int) -> np.ndarray:
    dst = blank()
    color = FIELDS[kind]
    dst[..., :3] = color
    dst[..., 3] = 1.0
    vig = ((XX - CX) / 380.0) ** 2 + ((YY - CY) / 380.0) ** 2
    dark = kind in ("grove", "dusk", "hearth")
    wash = mix(color, shade(color, 0.18 if dark else 0.08), clamp01(vig * 0.55)[..., None])
    wash = mix(wash, lite(color, 0.12), clamp01(1.0 - vig * 1.4)[..., None] * 0.35)
    dst[..., :3] = np.clip(wash * (1.0 + grain(17 + sum(ord(c) for c in kind), 0.03)[..., None]), 0.0, 1.0)
    ellipse(dst, CX, CY + RY + 36, 128, 22, shade(color, 0.30), 0.34 if not dark else 0.48, soft=16.0)
    if kind == "grove":
        disc(dst, 86, 86, 28, rgb("6aaa52"), 0.18, soft=20.0)
        disc(dst, 420, 400, 36, rgb("c4a04a"), 0.16, soft=22.0)
    elif kind == "snow":
        rng = np.random.RandomState(21)
        for _ in range(28):
            disc(
                dst,
                float(rng.uniform(18, 494)),
                float(rng.uniform(18, 220)),
                float(rng.uniform(1.2, 3.2)),
                rgb("ffffff"),
                float(rng.uniform(0.35, 0.88)),
                soft=1.1,
            )
    elif kind == "dusk":
        disc(dst, 410, 86, 34, rgb("f0c14a"), 0.20, soft=26.0)
        disc(dst, 416, 90, 12, rgb("fff6c8"), 0.55, soft=8.0)
    else:
        disc(dst, 92, 92, 40, rgb("e07028"), 0.22, soft=28.0)
        disc(dst, 98, 96, 14, rgb("fff0b0"), 0.40, soft=10.0)
    return dst


def paint_pelt(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    pal = PELTS[kind]
    fur, cream, ear, pad = pal["fur"], pal["cream"], pal["ear"], pal["pad"]
    dy = hover_y(frame)
    cx, cy = CX, CY + dy
    hx, hy = HEAD_X, HEAD_Y + dy

    nx, ny, nz, a = fox_volume(cx, cy)
    nx, ny, nz = bump_normals(nx, ny, nz, 90 + sum(ord(c) for c in kind), 0.055)
    outline = blank()
    onx, ony, onz, oa = fox_volume(cx, cy, RX + LINE_W, RY + LINE_W)
    blit_soft(outline, LINE, oa * 0.96)
    over(dst, outline)

    albedo = np.broadcast_to(fur, (H, W, 3)).copy()
    fold_t = clamp01(((YY - cy) / RY) * 0.40 + 0.16)
    albedo = mix(albedo, shade(fur, 0.18), fold_t)
    blit_volume(dst, albedo, nx, ny, nz, a, spec=0.16, shininess=14.0, sss=0.28)

    # Cream chest circle and 3/4 muzzle.
    volume_ball(dst, cx + 10, cy + 18, 52, 46, cream, width=3.2, spec=0.18, shininess=16.0, sss=0.22, bump=17)
    volume_ball(dst, hx + 22, hy + 12, 46, 38, cream, width=3.0, spec=0.20, shininess=16.0, sss=0.20, bump=23)

    # Pointed ears — left recedes, right reads larger.
    outlined_poly(
        dst,
        [(hx - 46, hy - 52), (hx - 78, hy - 118), (hx - 18, hy - 48)],
        shade(fur, 0.10),
        width=4.2,
    )
    fill_poly(dst, [(hx - 44, hy - 58), (hx - 68, hy - 104), (hx - 26, hy - 54)], ear)
    outlined_poly(
        dst,
        [(hx + 22, hy - 62), (hx + 72, hy - 136), (hx + 50, hy - 54)],
        fur,
        width=4.4,
    )
    fill_poly(dst, [(hx + 28, hy - 68), (hx + 62, hy - 118), (hx + 46, hy - 58)], ear)

    # Cheek tufts
    volume_ball(dst, hx - 48, hy + 22, 22, 18, fur, width=3.2, spec=0.14, shininess=12.0)
    volume_ball(dst, hx + 58, hy + 16, 24, 18, fur, width=3.2, spec=0.16, shininess=12.0)

    # Nose
    fill_poly(
        dst,
        [(hx + 28, hy + 8), (hx + 42, hy + 8), (hx + 35, hy + 18)],
        rgb("2a1c14"),
    )

    # Paw pads
    disc(dst, cx - 46, cy + RY * 0.72, 6.0, pad, 0.88, soft=1.4)
    disc(dst, cx + 46, cy + RY * 0.76, 6.2, pad, 0.88, soft=1.4)

    catch = blank()
    disc(catch, hx - 18, hy - 28, 28, rgb("ffffff"), 0.16 if kind != "dusk" else 0.10, soft=22.0)
    catch[..., 3] *= a
    over(dst, catch)
    return dst


def draw_eye(dst: np.ndarray, ex: float, ey: float, radius: float, closed: float, kind: str, lid: np.ndarray) -> None:
    if closed >= 0.85:
        outlined_ellipse(dst, ex, ey + 2, radius * 0.94, 6.2, LINE, width=3.2, cel=False)
        return
    if kind == "spark":
        radius *= 1.08
    ink = rgb("121010")
    if kind == "heart":
        ink = rgb("3a1418")
    outline_disk(dst, ex, ey, radius, radius, width=5.0)
    nx, ny, nz, a = ellipsoid(ex, ey, radius, radius, soft=1.2)
    blit_volume(dst, ink, nx, ny, nz, a, spec=0.62, shininess=36.0, sss=0.04, ambient=0.16, wrap=0.12)
    if kind == "heart":
        pr = radius * 0.42
        fill_poly(
            dst,
            [
                (ex, ey + pr * 0.72),
                (ex - pr * 0.72, ey - 2),
                (ex - pr * 0.22, ey - pr * 0.55),
                (ex, ey - pr * 0.18),
                (ex + pr * 0.22, ey - pr * 0.55),
                (ex + pr * 0.72, ey - 2),
            ],
            rgb("f08aa0"),
        )
    else:
        disc(dst, ex - radius * 0.30, ey - radius * 0.32, radius * 0.28, rgb("ffffff"), 0.98, soft=1.0)
        disc(dst, ex + radius * 0.22, ey + radius * 0.18, radius * 0.12, rgb("ffffff"), 0.84, soft=0.8)
        if kind == "spark":
            disc(dst, ex + radius * 0.02, ey - radius * 0.04, radius * 0.08, rgb("fff6c8"), 0.92, soft=0.7)
    if closed > 0.2:
        lid_layer = blank()
        ellipse(lid_layer, ex, ey - radius * (1.2 - closed * 0.95), radius * 1.12, radius * 0.92, lid, 1.0)
        clip_disc(lid_layer, ex, ey, radius + 1.2)
        over(dst, lid_layer)


def paint_mug(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    dy = hover_y(frame)
    closed = blink_amount(frame)
    if kind == "sleepy":
        closed = 1.0
    if kind == "wink":
        left_closed, right_closed = 1.0, closed
    else:
        left_closed = right_closed = closed
    # 3/4 face: left eye recedes, right eye is larger.
    lx, ly = HEAD_X - 18.0, HEAD_Y - 18.0 + dy
    rx, ry = HEAD_X + 38.0, HEAD_Y - 24.0 + dy
    lid = rgb("f8e2c4")
    draw_eye(dst, lx, ly, 22.0, left_closed, kind, lid)
    draw_eye(dst, rx, ry, 28.0, right_closed, kind, lid)

    mx, my = HEAD_X + 24.0, HEAD_Y + 28.0 + dy
    if kind == "grin":
        ellipse(dst, mx, my + 4, 14, 5.0, LINE, 0.88, soft=1.2)
    elif kind == "pout":
        ellipse(dst, mx, my + 6, 8, 3.2, LINE, 0.86, soft=1.0)
    elif kind == "blep":
        outlined_ellipse(dst, mx + 4, my + 8, 7.2, 10, rgb("f09098"), width=2.8, cel=False)
    elif kind == "heart":
        outlined_ellipse(dst, mx, my + 4, 6.5, 4.2, rgb("e06a7a"), width=2.8, cel=False)
    elif kind == "sleepy":
        ellipse(dst, mx, my + 2, 6.5, 2.8, LINE, 0.8, soft=1.0)
    elif kind in ("blink", "spark"):
        outlined_ellipse(dst, mx + 2, my + 6, 6.4, 5.2, rgb("f09098"), width=2.6, cel=False)
    return dst


def paint_hat(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    if kind == "none":
        return dst
    dy = hover_y(frame)
    x, y = HAT_X, HAT_Y + dy
    if kind == "beret":
        volume_ball(dst, x + 10, y + 18, 52, 20, rgb("3a4468"), width=4.4, spec=0.14, shininess=12.0)
        volume_ball(dst, x + 28, y + 4, 16, 12, rgb("2a3454"), width=3.2, spec=0.16, shininess=12.0)
    elif kind == "cap":
        volume_ball(dst, x + 4, y + 20, 48, 18, rgb("4a5a42"), width=4.2, spec=0.14, shininess=12.0)
        outlined_ellipse(dst, x + 36, y + 28, 30, 8, rgb("5a6a50"), width=3.2, cel=False)
    elif kind == "flower":
        for i in range(5):
            ang = i * (2.0 * math.pi / 5.0) - 0.3
            volume_ball(
                dst,
                x + 10 + math.cos(ang) * 22,
                y + 16 + math.sin(ang) * 14,
                11,
                11,
                rgb("f0b0c0"),
                width=3.0,
                spec=0.22,
                shininess=16.0,
                sss=0.20,
            )
        volume_ball(dst, x + 10, y + 16, 9, 9, rgb("f0c14a"), width=2.8, spec=0.30, shininess=20.0)
    elif kind == "leaf":
        outlined_poly(
            dst,
            [(x - 4, y + 28), (x + 36, y - 10), (x + 10, y + 32)],
            rgb("c45a28"),
            width=3.6,
        )
        fill_poly(dst, [(x + 2, y + 22), (x + 32, y - 2), (x + 12, y + 26)], rgb("e07028"))
    elif kind == "beanie":
        volume_ball(dst, x + 2, y + 22, 50, 22, rgb("a84850"), width=4.4, spec=0.16, shininess=12.0)
        volume_ball(dst, x + 4, y + 2, 9, 9, rgb("f4efe6"), width=2.8, spec=0.22, shininess=16.0)
    elif kind == "bow":
        volume_ball(dst, x - 16, y + 14, 20, 14, rgb("e06a8a"), width=3.6, spec=0.22, shininess=16.0)
        volume_ball(dst, x + 28, y + 14, 20, 14, rgb("e06a8a"), width=3.6, spec=0.22, shininess=16.0)
        volume_ball(dst, x + 6, y + 14, 9, 9, rgb("c43c5a"), width=3.0, spec=0.24, shininess=18.0)
    return dst


def paint_wrap(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    if kind == "none":
        return dst
    dy = hover_y(frame)
    x, y = WRAP_X, WRAP_Y + dy
    if kind == "scarf":
        volume_ball(dst, x, y, 78, 16, rgb("e07028"), width=4.2, spec=0.16, shininess=12.0)
        volume_ball(dst, x + 8, y + 6, 70, 10, rgb("2a2430"), width=3.4, spec=0.12, shininess=10.0)
        outlined_poly(
            dst,
            [(x + 40, y + 4), (x + 78, y + 36), (x + 62, y + 44), (x + 28, y + 12)],
            rgb("e07028"),
            width=3.6,
        )
    elif kind == "bandana":
        volume_ball(dst, x, y - 2, 70, 14, rgb("c43c3c"), width=4.0, spec=0.16, shininess=12.0)
        outlined_poly(
            dst,
            [(x + 48, y - 2), (x + 78, y + 24), (x + 52, y + 10)],
            rgb("e05a5a"),
            width=3.2,
        )
    elif kind == "bell":
        volume_ball(dst, x, y, 62, 12, rgb("2a2430"), width=3.8, spec=0.12, shininess=10.0)
        volume_ball(dst, x + 6, y + 16, 11, 12, rgb("f0c14a"), width=2.8, spec=0.36, shininess=22.0)
    return dst


def paint_charm(kind: str, frame: int) -> np.ndarray:
    dst = blank()
    if kind == "none":
        return dst
    bob = hover_y(frame) + math.sin((frame + 3) / FRAMES * math.pi * 2.0) * 2.4
    x, y = CHARM_X, CHARM_Y + bob
    if kind == "acorn":
        volume_ball(dst, x, y + 6, 14, 16, rgb("8a5a28"), width=3.2, spec=0.18, shininess=14.0)
        volume_ball(dst, x, y - 8, 16, 10, rgb("5a3a1c"), width=3.0, spec=0.16, shininess=12.0)
    elif kind == "leaf":
        outlined_poly(
            dst,
            [(x - 8, y + 12), (x + 20, y - 18), (x + 4, y + 16)],
            rgb("c45a28"),
            width=3.2,
        )
    elif kind == "lantern":
        volume_ball(dst, x, y, 16, 18, rgb("f0c14a"), width=3.4, spec=0.28, shininess=20.0, sss=0.16)
        volume_ball(dst, x, y - 16, 8, 6, rgb("8a6a40"), width=2.6, spec=0.14, shininess=10.0)
        disc(dst, x - 3, y - 2, 4, rgb("fff6c8"), 0.45, soft=2.0)
    return dst


TRAIT_SPEC = {
    "field": [
        ("grove", "Grove", 32),
        ("snow", "Snow", 26),
        ("dusk", "Dusk", 24),
        ("hearth", "Hearth", 18),
    ],
    "pelt": [
        ("maple", "Maple", 55),
        ("snow", "Snow", 28),
        ("dusk", "Dusk", 17),
    ],
    "mug": [
        ("blink", "Normal", 20),
        ("grin", "Grin", 16),
        ("sleepy", "Sleepy", 14),
        ("blep", "Blep", 12),
        ("wink", "Wink", 12),
        ("spark", "Sparkly", 10),
        ("pout", "Pout", 9),
        ("heart", "Heart", 7),
    ],
    "hat": [
        ("none", "None", 28),
        ("leaf", "Leaf", 16),
        ("beret", "Beret", 14),
        ("flower", "Flower", 12),
        ("beanie", "Beanie", 12),
        ("cap", "Cap", 10),
        ("bow", "Bow", 8),
    ],
    "wrap": [
        ("none", "None", 40),
        ("scarf", "Scarf", 24),
        ("bandana", "Bandana", 20),
        ("bell", "Bell", 16),
    ],
    "charm": [
        ("none", "None", 40),
        ("acorn", "Acorn", 24),
        ("leaf", "Leaf", 20),
        ("lantern", "Lantern", 16),
    ],
}

PAINTERS = {
    "field": {k: (lambda kind: (lambda frame, k=kind: paint_field(k, frame)))(k) for k in FIELDS},
    "pelt": {k: (lambda kind: (lambda frame, k=kind: paint_pelt(k, frame)))(k) for k in PELTS},
    "mug": {k: (lambda kind: (lambda frame, k=kind: paint_mug(k, frame)))(k) for k in MUGS},
    "hat": {k: (lambda kind: (lambda frame, k=kind: paint_hat(k, frame)))(k) for k in HATS},
    "wrap": {k: (lambda kind: (lambda frame, k=kind: paint_wrap(k, frame)))(k) for k in WRAPS},
    "charm": {k: (lambda kind: (lambda frame, k=kind: paint_charm(k, frame)))(k) for k in CHARMS},
}

STACK = ("field", "pelt", "mug", "hat", "wrap", "charm")

SIGNATURES = [
    {"field": "grove", "pelt": "maple", "mug": "blink", "hat": "none", "wrap": "none", "charm": "none"},
    {"field": "grove", "pelt": "maple", "mug": "grin", "hat": "leaf", "wrap": "scarf", "charm": "acorn"},
    {"field": "dusk", "pelt": "dusk", "mug": "spark", "hat": "beret", "wrap": "bandana", "charm": "lantern"},
    {"field": "snow", "pelt": "snow", "mug": "sleepy", "hat": "beanie", "wrap": "none", "charm": "none"},
    {"field": "hearth", "pelt": "maple", "mug": "wink", "hat": "cap", "wrap": "bell", "charm": "leaf"},
    {"field": "grove", "pelt": "snow", "mug": "blep", "hat": "flower", "wrap": "scarf", "charm": "acorn"},
    {"field": "dusk", "pelt": "maple", "mug": "pout", "hat": "none", "wrap": "bandana", "charm": "lantern"},
    {"field": "snow", "pelt": "dusk", "mug": "grin", "hat": "leaf", "wrap": "none", "charm": "leaf"},
    {"field": "hearth", "pelt": "snow", "mug": "spark", "hat": "beret", "wrap": "scarf", "charm": "none"},
    {"field": "grove", "pelt": "dusk", "mug": "sleepy", "hat": "cap", "wrap": "bell", "charm": "acorn"},
    {"field": "dusk", "pelt": "snow", "mug": "wink", "hat": "flower", "wrap": "none", "charm": "lantern"},
    {"field": "hearth", "pelt": "dusk", "mug": "heart", "hat": "beanie", "wrap": "bandana", "charm": "leaf"},
    {"field": "snow", "pelt": "maple", "mug": "grin", "hat": "bow", "wrap": "bell", "charm": "acorn"},
    {"field": "grove", "pelt": "maple", "mug": "spark", "hat": "beret", "wrap": "none", "charm": "none"},
    {"field": "dusk", "pelt": "snow", "mug": "sleepy", "hat": "leaf", "wrap": "scarf", "charm": "lantern"},
    {"field": "hearth", "pelt": "maple", "mug": "blep", "hat": "flower", "wrap": "none", "charm": "leaf"},
]

TRAIT_LABELS = (
    ("field", "Field"),
    ("pelt", "Pelt"),
    ("mug", "Mug"),
    ("hat", "Hat"),
    ("wrap", "Wrap"),
    ("charm", "Charm"),
)

COLLECTION_DESCRIPTION = (
    "Foxkins is a 5,555-piece collection of looping clay fox PFP GIFs. "
    "Each Foxkin is stacked from six layers — field, pelt, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. "
    "Three pelts. One locked three-quarter loaf-orb. Hats sit between the ears. The silhouette never changes shape."
)

COLLECTION_STORY = (
    "Foxkins.\n\n"
    "A 5,555-piece collection of looping clay fox PFP GIFs. "
    "Each Foxkin is stacked from six layers — field, pelt, mug, hat, wrap, and charm — then flattened onto one 12-frame GIF. "
    "Three pelts only: maple, snow, and dusk. The loaf-orb never gets a special cutout. "
    "Hats sit between the ears. Scarves sit on the neck. Charms float by the tucked paws.\n\n"
    "Painted 3D clay — canvas grain, wrap shade, a warm key from the left. "
    "Mix 3 three-quarter pose. Croissant tail on the left. Cream muzzle facing right. One shared clock.\n\n"
    "Minting on Base (chain ID 8453). Gas is ETH."
)


def trait_path(category: str, trait_id: str) -> Path:
    return TRAIT_DIR / category / f"{trait_id}.png"


def render_trait_frames(category: str, trait_id: str) -> list[Image.Image]:
    paint = PAINTERS[category][trait_id]
    return [to_image(paint(frame)) for frame in range(FRAMES)]


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
        "name": "Foxkins",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Three pelt bodies share one Mix 3 skeleton; hats, wraps, and charms never edit the pelt.",
    }
    (TRAIT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def build_samples() -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    samples = []
    for index, selection in enumerate(SIGNATURES, start=1):
        print(f"  sample #{index}")
        frames = compose_selection(selection)
        save_loop_gif(frames, PREVIEW_DIR / f"{index}.gif", DURATION_MS, colors=180)
        samples.append(
            {
                "id": index,
                "name": f"Foxkin #{index}",
                "image": f"/foxkins-preview/{index}.gif",
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
            f'    image: "{sample["image"]}?v=1",\n'
            f"    attributes: [\n      {attrs},\n    ],\n"
            "  }"
        )
    (SRC_DATA / "foxkin-gallery.ts").write_text(
        "export type FoxkinSample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const foxkinSamples: FoxkinSample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = [FIELDS["dusk"], FIELDS["grove"], rgb("e87a3a"), FIELDS["hearth"]]
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)
    y = np.linspace(0.0, 1.0, height, dtype=np.float32)
    xx, yy = np.meshgrid(x, y)
    stops = np.stack(colors, axis=0)
    t = np.clip(xx * 0.72 + yy * 0.28, 0.0, 0.999) * (len(colors) - 1)
    i0 = np.floor(t).astype(np.int32)
    f = (t - i0)[..., None]
    c0 = stops[i0]
    c1 = stops[np.clip(i0 + 1, 0, len(colors) - 1)]
    rgb_out = c0 * (1.0 - f) + c1 * f
    arr = np.dstack([np.clip(rgb_out * 255.0, 0, 255).astype(np.uint8), np.full((height, width), 255, dtype=np.uint8)])
    return Image.fromarray(arr, "RGBA")


def write_collection_meta() -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    (META_DIR / "foxkins-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "foxkins.json").write_text(
        json.dumps(
            {
                "name": "Foxkins",
                "symbol": "FOXK",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-foxkins.gif",
                "featured_image": "/brand/featured-foxkins.jpg",
                "banner_image": "/brand/banner-foxkins.png",
                "opensea_banner_image": "/brand/banner-foxkins-opensea.jpg",
                "external_link": "/foxkins",
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
    logo_frames = compose_selection(SIGNATURES[1])

    logo = logo_frames[0].copy()
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse((18, 18, SIZE - 18, SIZE - 18), fill=255)
    logo.putalpha(Image.composite(logo.split()[-1], Image.new("L", (SIZE, SIZE), 0), mask))
    ring = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((10, 10, SIZE - 10, SIZE - 10), outline=(232, 122, 58, 230), width=10)
    logo = Image.alpha_composite(logo, ring)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-foxkins.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-foxkins-loop.png",
    )

    def fox_lineup(width: int, height: int, faces: list[Image.Image]) -> Image.Image:
        canvas = panoramic_wash(width, height)
        count = len(faces)
        size = int(height * 0.82)
        overlap = size // 5
        total = size * count - overlap * (count - 1)
        start_x = (width - total) // 2
        y = (height - size) // 2 + int(height * 0.04)
        for index, portrait in enumerate(faces):
            x = start_x + index * (size - overlap)
            place_portrait(canvas, portrait, x, y, size, radius=max(36, size // 10))
        return canvas

    save_image(fox_lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-foxkins.png", quality=94)
    save_image(fox_lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-foxkins-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[1], 90, 110, 560, radius=64)
    place_portrait(featured, portraits[3], 540, 130, 560, radius=64)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-foxkins.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(gif_frames, BRAND_DIR / "collection-foxkins.gif", DURATION_MS, colors=180)
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true")
    parser.add_argument("--hats-only", action="store_true")
    parser.add_argument("--hat", action="append", dest="hats")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Foxkins brand kit…")
        build_brand()
        print("Done.")
        return
    if args.hats_only:
        print("Rebuilding Foxkins hat layers…")
        build_traits(only="hat", ids=args.hats)
        print("Compositing sample GIF tokens…")
        build_samples()
        print("Writing brand…")
        build_brand()
        print("Done.")
        return
    print("Building Foxkins Mix 3 trait loops…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
