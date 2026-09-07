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


Pt = tuple[float, float]
DOWN = math.pi / 2
UP = -math.pi / 2
TORSO_LEN = 124.0
UPPER_ARM = 54.0
FOREARM = 50.0
THIGH = 66.0
SHIN = 70.0
FLOOR_Y = 436.0


def polar(point: Pt, ang: float, length: float) -> Pt:
    return (point[0] + math.cos(ang) * length, point[1] + math.sin(ang) * length)


def lerp(a: Pt, b: Pt, u: float) -> Pt:
    return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)


def dist(a: Pt, b: Pt) -> float:
    return math.hypot(b[0] - a[0], b[1] - a[1])


def rotate(point: Pt, origin: Pt, ang: float) -> Pt:
    dx, dy = point[0] - origin[0], point[1] - origin[1]
    ca, sa = math.cos(ang), math.sin(ang)
    return (origin[0] + dx * ca - dy * sa, origin[1] + dx * sa + dy * ca)


def electrode(draw: ImageDraw.ImageDraw, x: int, y: int, core: int) -> None:
    cap = max(3, core // 2 + 1)
    draw.ellipse((x - cap, y - cap + 1, x + cap, y + cap + 2), fill=(36, 32, 40, 255))
    draw.ellipse((x - cap + 1, y - cap, x + cap - 1, y + cap - 2), fill=(90, 86, 96, 255))


def glow_polylines(
    canvas: Image.Image,
    polylines: list[list[tuple[float, float]]],
    color: tuple[int, int, int],
    core: int = 7,
    halo: int = 28,
    halo_alpha: int = 110,
    hot: tuple[int, int, int] = (255, 252, 240),
    electrodes: bool = True,
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
        if electrodes:
            for cx, cy in (xy[0], xy[-1]):
                electrode(draw, cx, cy, core)


def sample_curve(fn, n: int = 40) -> list[tuple[float, float]]:
    return [fn(i / (n - 1)) for i in range(n)]


def glass(a: Pt, b: Pt, bulge: float = 0.0, n: int = 14, overlap: float = 3.5) -> list[Pt]:
    """Tube from a to b. A short overlap at a fuses the joint without stabbing through the torso."""
    span = dist(a, b) or 1.0
    start = lerp(a, b, -min(overlap / span, 0.08))
    if n < 2:
        return [start, b]
    if abs(bulge) < 0.4:
        return [lerp(start, b, i / (n - 1)) for i in range(n)]
    dx, dy = b[0] - start[0], b[1] - start[1]
    ln = math.hypot(dx, dy) or 1.0
    ctrl = ((start[0] + b[0]) / 2 - dy / ln * bulge, (start[1] + b[1]) / 2 + dx / ln * bulge)
    pts: list[Pt] = []
    for i in range(n):
        u = i / (n - 1)
        om = 1.0 - u
        pts.append(
            (
                om * om * start[0] + 2 * om * u * ctrl[0] + u * u * b[0],
                om * om * start[1] + 2 * om * u * ctrl[1] + u * u * b[1],
            )
        )
    return pts


def smoothstep(u: float) -> float:
    u = max(0.0, min(1.0, u))
    return u * u * (3.0 - 2.0 * u)


def perp_of(a: Pt, b: Pt, scale: float) -> Pt:
    dx, dy = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(dx, dy) or 1.0
    return (-dy / ln * scale, dx / ln * scale)


def bezier_through(a: Pt, mid: Pt, b: Pt, n: int = 22) -> list[Pt]:
    """One glass tube that actually bends through the elbow or knee."""
    ctrl = (2 * mid[0] - 0.5 * (a[0] + b[0]), 2 * mid[1] - 0.5 * (a[1] + b[1]))
    pts: list[Pt] = []
    for i in range(n):
        u = i / (n - 1)
        om = 1.0 - u
        pts.append(
            (
                om * om * a[0] + 2 * om * u * ctrl[0] + u * u * b[0],
                om * om * a[1] + 2 * om * u * ctrl[1] + u * u * b[1],
            )
        )
    return pts


def cubic(a: Pt, c1: Pt, c2: Pt, b: Pt, n: int = 24) -> list[Pt]:
    pts: list[Pt] = []
    for i in range(n):
        u = i / (n - 1)
        om = 1.0 - u
        pts.append(
            (
                om**3 * a[0] + 3 * om * om * u * c1[0] + 3 * om * u * u * c2[0] + u**3 * b[0],
                om**3 * a[1] + 3 * om * om * u * c1[1] + 3 * om * u * u * c2[1] + u**3 * b[1],
            )
        )
    return pts


def two_bone_ik(origin: Pt, target: Pt, upper: float, lower: float, bend: float) -> tuple[Pt, Pt]:
    dx = target[0] - origin[0]
    dy = target[1] - origin[1]
    span = math.hypot(dx, dy) or 0.001
    reach = min(max(span, abs(upper - lower) + 0.8), upper + lower - 0.8)
    ux, uy = dx / span, dy / span
    end = (origin[0] + ux * reach, origin[1] + uy * reach)
    cos_a = (upper * upper + reach * reach - lower * lower) / (2.0 * upper * reach)
    a = math.acos(max(-1.0, min(1.0, cos_a)))
    base = math.atan2(end[1] - origin[1], end[0] - origin[0])
    mid = polar(origin, base + a * bend, upper)
    return mid, end


def two_bone_fk(origin: Pt, ang: float, upper: float, flex: float, lower: float) -> tuple[Pt, Pt]:
    mid = polar(origin, ang, upper)
    end = polar(mid, ang + flex, lower)
    return mid, end


def head_loop(neck: Pt, tilt: float, rx: float = 22.0, ry: float = 28.0) -> list[Pt]:
    """Closed oval whose bottom sits on the neck so the head never floats off."""
    cx, cy = neck[0], neck[1] - ry
    pts: list[Pt] = []
    steps = 28
    for i in range(steps + 1):
        a = math.pi / 2 + i / steps * 2 * math.pi
        pts.append(rotate((cx + math.cos(a) * rx, cy + math.sin(a) * ry), neck, tilt))
    return pts


def _shift(paths: list[list[Pt]], tips: list[Pt], welds: list[Pt], dx: float, dy: float) -> tuple[list[list[Pt]], list[Pt], list[Pt]]:
    if dx == 0 and dy == 0:
        return paths, tips, welds
    return (
        [[(x + dx, y + dy) for x, y in path] for path in paths],
        [(x + dx, y + dy) for x, y in tips],
        [(x + dx, y + dy) for x, y in welds],
    )


def seat_figure(paths: list[list[Pt]], tips: list[Pt], welds: list[Pt]) -> tuple[list[list[Pt]], list[Pt], list[Pt]]:
    pts = [p for path in paths for p in path]
    if not pts:
        return paths, tips, welds
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    dx = dy = 0.0
    margin = 30.0
    if min(xs) < margin:
        dx = margin - min(xs)
    elif max(xs) > SIZE - margin:
        dx = SIZE - margin - max(xs)
    if min(ys) < margin:
        dy = margin - min(ys)
    elif max(ys) > SIZE - 16:
        dy = SIZE - 16 - max(ys)
    return _shift(paths, tips, welds, dx, dy)


def bend_figure(kind: str, frame: int) -> tuple[list[list[Pt]], list[Pt], list[Pt]]:
    """Connected neon dancer: joints parented, tubes drawn as one bent glass path."""
    t = clock(frame) + {
        "sway": 0.85,
        "kick": 0.55,
        "wave": 1.05,
        "hop": 0.7,
        "point": 0.9,
        "dip": 0.65,
        "spin": 0.4,
        "split": 0.75,
    }.get(kind, 0.0)
    s = math.sin(t)
    c = math.cos(t)
    s2 = math.sin(t * 2)
    s_lag = math.sin(t - 0.45)
    hip: Pt = (256.0, 322.0)
    lean = 0.0
    head_tilt = 0.0
    sh_w, hip_w = 8.0, 6.0
    depth = 1.0
    arch = 16.0
    l_arm = (DOWN + 0.55, 0.4)
    r_arm = (DOWN - 0.55, -0.4)
    wave_r = False
    l_foot: Pt = (238.0, FLOOR_Y)
    r_foot: Pt = (274.0, FLOOR_Y)
    l_ik = r_ik = True
    l_fk = (DOWN + 0.12, 0.22)
    r_fk = (DOWN - 0.12, -0.22)
    l_knee_out, r_knee_out = 1.0, -1.0

    if kind == "sway":
        hip = (256.0 + s * 32.0, 320.0 + abs(s) * 14.0 - s2 * 8.0)
        lean = s * 0.5
        head_tilt = s_lag * 0.4
        arch = 22.0 + 8.0 * c
        l_foot = (226.0 + s * 16.0, FLOOR_Y)
        r_foot = (286.0 + s * 16.0, FLOOR_Y)
        l_arm = (DOWN + 0.45 - max(0.0, s) * 2.2, 0.95 + 0.25 * c)
        r_arm = (DOWN - 0.45 + max(0.0, -s) * 2.2, -0.95 - 0.25 * c)
    elif kind == "kick":
        k = smoothstep((s + 1.0) * 0.5)
        hip = (248.0 - k * 12.0, 318.0 - k * 16.0 + (1.0 - k) * abs(s2) * 8.0)
        lean = -0.18 - k * 0.38
        head_tilt = -0.12 - k * 0.1
        arch = 14.0 + 10.0 * k
        l_foot = (222.0, FLOOR_Y - (1.0 - k) * 5.0)
        r_ik = False
        r_fk = (DOWN - 0.12 - k * 2.2, 1.15 - k * 1.35)
        l_arm = (UP + 0.2 + k * 0.55, 0.85 + 0.15 * c)
        r_arm = (DOWN + 0.15 - k * 0.35, -0.95)
    elif kind == "wave":
        hip = (256.0 + s * 12.0, 320.0 - abs(s2) * 10.0)
        lean = 0.2 + s * 0.16
        head_tilt = 0.18 + s_lag * 0.16
        arch = 18.0 + 6.0 * s
        l_foot = (234.0 + s * 6.0, FLOOR_Y)
        r_foot = (278.0 + s * 6.0, FLOOR_Y)
        l_arm = (DOWN + 0.55 + s * 0.55, 0.95 + 0.2 * c)
        r_arm = (DOWN - 0.2, -0.2)
        wave_r = True
    elif kind == "hop":
        lift = max(0.0, s) ** 1.15 * 56.0
        squat = max(0.0, -s) * 24.0
        tuck = max(0.0, s) * 30.0
        hip = (256.0 + s_lag * 8.0, 322.0 - lift + squat)
        lean = s * 0.14
        head_tilt = s_lag * 0.22
        arch = 12.0 + 10.0 * max(0.0, s)
        l_foot = (230.0, FLOOR_Y - lift + tuck)
        r_foot = (282.0, FLOOR_Y - lift + tuck)
        reach = max(0.0, s_lag)
        l_arm = (UP + 1.05 - reach * 0.85, 0.85)
        r_arm = (UP - 1.05 + reach * 0.85, -0.85)
    elif kind == "point":
        hip = (240.0 + s * 8.0, 322.0 - abs(s) * 8.0)
        lean = 0.64 + s * 0.14
        head_tilt = 0.28 + s_lag * 0.12
        arch = 20.0 + 6.0 * s
        l_foot = (208.0, FLOOR_Y)
        r_foot = (274.0 + s * 12.0, FLOOR_Y - 14.0 - abs(s) * 8.0)
        l_arm = (math.pi * 0.88 + s * 0.2, 0.7 + 0.15 * c)
        r_arm = (-0.58 + s * 0.14, 0.18)
    elif kind == "dip":
        hip = (276.0 + s * 12.0, 328.0 - abs(s) * 8.0)
        lean = 0.88 + s * 0.2
        head_tilt = 0.58 + s_lag * 0.22
        arch = 30.0 + 10.0 * s
        l_foot = (190.0, FLOOR_Y)
        r_foot = (334.0, FLOOR_Y - 6.0)
        l_arm = (DOWN + 0.4 + s * 0.5, 0.85)
        r_arm = (UP - 0.15 + s * 0.35, -0.95)
    elif kind == "spin":
        depth = c
        hip = (256.0 + s * 10.0, 320.0 + abs(s) * 10.0)
        lean = s * 0.24
        head_tilt = s_lag * 0.28
        arch = 16.0 + 8.0 * s
        l_foot = (240.0 + s * 22.0, FLOOR_Y - max(0.0, -c) * 18.0)
        r_foot = (272.0 - s * 22.0, FLOOR_Y - max(0.0, c) * 18.0)
        l_arm = (math.pi + 0.15 * s, 0.75 + 0.15 * c)
        r_arm = (-0.05 * s, -0.75 - 0.15 * c)
    else:
        reach = THIGH + SHIN - 6.0
        spread = 112.0 + abs(s) * 12.0
        drop = math.sqrt(max(64.0, reach * reach - spread * spread))
        hip = (256.0, FLOOR_Y - drop + abs(s2) * 8.0)
        lean = s * 0.12
        head_tilt = s_lag * 0.14
        arch = 14.0
        l_foot = (256.0 - spread - s * 8.0, FLOOR_Y)
        r_foot = (256.0 + spread + s * 8.0, FLOOR_Y)
        l_arm = (UP + 0.7 + s * 0.4, 0.7)
        r_arm = (UP - 0.7 - s * 0.4, -0.7)
        l_knee_out, r_knee_out = -1.0, 1.0

    dw = math.copysign(max(0.32, abs(depth)), depth)
    neck = polar(hip, UP + lean, TORSO_LEN)
    neck_into_head = polar(neck, UP + lean, 10.0)
    ox, oy = perp_of(hip, neck, arch * (s if kind != "spin" else 1.0))
    if kind == "spin":
        ox, oy = perp_of(hip, neck, arch * s)
    waist = lerp(hip, neck, 0.36)
    chest = lerp(hip, neck, 0.72)
    waist = (waist[0] + ox, waist[1] + oy)
    chest = (chest[0] - ox * 0.55, chest[1] - oy * 0.55)
    sh_anchor = chest
    l_sh = (sh_anchor[0] - sh_w * dw, sh_anchor[1] + 2.0)
    r_sh = (sh_anchor[0] + sh_w * dw, sh_anchor[1] + 2.0)
    l_hip = (hip[0] - hip_w * dw, hip[1] + 2.0)
    r_hip = (hip[0] + hip_w * dw, hip[1] + 2.0)

    if l_ik:
        l_knee, l_end = two_bone_ik(l_hip, l_foot, THIGH, SHIN, l_knee_out)
    else:
        l_knee, l_end = two_bone_fk(l_hip, l_fk[0], THIGH, l_fk[1], SHIN)
    if r_ik:
        r_knee, r_end = two_bone_ik(r_hip, r_foot, THIGH, SHIN, r_knee_out)
    else:
        r_knee, r_end = two_bone_fk(r_hip, r_fk[0], THIGH, r_fk[1], SHIN)

    l_elb, l_hand = two_bone_fk(l_sh, l_arm[0], UPPER_ARM, l_arm[1], FOREARM)
    wave_mid: Pt | None = None
    if wave_r:
        base = -0.28
        r_elb = polar(r_sh, base + s * 0.4, UPPER_ARM)
        wave_mid = polar(r_elb, base + 0.45 + math.sin(t + 0.9) * 1.2, FOREARM * 0.78)
        r_hand = polar(wave_mid, base + 0.15 + math.sin(t + 1.9) * 1.3, 38.0)
    else:
        r_elb, r_hand = two_bone_fk(r_sh, r_arm[0], UPPER_ARM, r_arm[1], FOREARM)

    squash = 1.0 + 0.08 * s2
    head = head_loop(neck, head_tilt, rx=22.0 * squash, ry=28.0 / squash)
    if wave_mid is not None:
        right_arm = cubic(chest, r_elb, wave_mid, r_hand, n=28)
    else:
        right_arm = bezier_through(chest, r_elb, r_hand)
    tubes = [
        head,
        cubic(hip, waist, chest, neck_into_head),
        bezier_through(chest, l_elb, l_hand),
        right_arm,
        bezier_through(hip, l_knee, l_end),
        bezier_through(hip, r_knee, r_end),
    ]
    tips = [l_hand, r_hand, l_end, r_end]
    welds: list[Pt] = []
    return seat_figure(tubes, tips, welds)


def paint_bend(kind: str, frame: int) -> Image.Image:
    layer = blank()
    tubes, tips, _welds = bend_figure(kind, frame)
    glow_polylines(layer, tubes, (236, 244, 255), core=8, halo=26, halo_alpha=80, electrodes=False)
    draw = ImageDraw.Draw(layer)
    for x, y in tips:
        electrode(draw, int(x), int(y), core=8)
    return layer


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
