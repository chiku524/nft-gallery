#!/usr/bin/env python3
"""Paint Groovy Nation — airbrushed 70s album-cover musical notes.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
Note, expression, topper, and cable share one bounce so faces stay on the head.
Venue stays a stage. Riff floats on its own pulse.

Look: airbrush chrome on real notation silhouettes. Tilted oval noteheads.
Thin stems. Flags and beams at the top. Faces live on the head, not a sphere.
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

from gif_bake import save_loop_gif  # noqa: E402
from paint_kit import DURATION_MS, FRAMES, SIZE, place_portrait, save_apng, save_image  # noqa: E402

TRAIT_DIR = ROOT / "public" / "groovy-traits"
PREVIEW_DIR = ROOT / "public" / "groovy-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

H = W = SIZE
YY, XX = np.indices((H, W), dtype=np.float32)

CX = 216.0
HEAD_Y = 338.0
HEAD_RX = 92.0
HEAD_RY = 54.0
HEAD_ANGLE = -33.0
NOTE_SHEAR = 0.42
STEM_LEN = 238.0
STEM_W = 8.8

VENUES = ("sunset", "lava", "checker", "velvet", "blacklight", "chrome")
NOTES = ("quarter", "eighth", "whole", "beamed")
EXPRESSIONS = ("cool", "shout", "wink", "groove", "star")
TOPPERS = ("none", "afro", "shades", "visor", "halo")
CABLES = ("none", "chain", "cans", "mic")
RIFFS = ("none", "treble", "vinyl", "stars", "bolt")

METAL = {
    "quarter": np.array([1.00, 0.74, 0.22], dtype=np.float32),
    "eighth": np.array([0.95, 0.28, 0.62], dtype=np.float32),
    "whole": np.array([0.92, 0.88, 1.00], dtype=np.float32),
    "beamed": np.array([0.22, 0.86, 0.78], dtype=np.float32),
}


def clamp01(arr: np.ndarray) -> np.ndarray:
    return np.clip(arr, 0.0, 1.0)


def smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = clamp01((x - edge0) / (edge1 - edge0 + 1e-6))
    return t * t * (3.0 - 2.0 * t)


def blank() -> np.ndarray:
    return np.zeros((H, W, 4), dtype=np.float32)


def to_image(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(arr * 255.0, 0, 255).astype(np.uint8), "RGBA")


def stamp(canvas: np.ndarray, color: np.ndarray, alpha: np.ndarray) -> None:
    a = clamp01(alpha)[..., None]
    rgb = np.asarray(color, dtype=np.float32)
    if rgb.ndim == 1:
        rgb = rgb[:3]
    else:
        rgb = rgb[..., :3]
    canvas[..., :3] = canvas[..., :3] * (1.0 - a) + rgb * a
    canvas[..., 3] = canvas[..., 3] + (1.0 - canvas[..., 3]) * a[..., 0]


def air_disc(cx: float, cy: float, radius: float, soft: float = 7.0) -> np.ndarray:
    dist = np.sqrt((XX - cx) ** 2 + (YY - cy) ** 2)
    return smoothstep(radius + soft, radius - soft, dist)


def rotate_xy(cx: float, cy: float, angle_deg: float) -> tuple[np.ndarray, np.ndarray]:
    ang = math.radians(angle_deg)
    cos_a, sin_a = math.cos(ang), math.sin(ang)
    dx = XX - cx
    dy = YY - cy
    return dx * cos_a + dy * sin_a, -dx * sin_a + dy * cos_a


def air_ellipse(cx: float, cy: float, rx: float, ry: float, angle_deg: float = 0.0, soft: float = 6.0) -> np.ndarray:
    xr, yr = rotate_xy(cx, cy, angle_deg)
    rad = np.sqrt((xr / max(rx, 1.0)) ** 2 + (yr / max(ry, 1.0)) ** 2)
    edge = soft / max(min(rx, ry), 1.0)
    return smoothstep(1.0 + edge, 1.0 - edge, rad)


def air_notehead(
    cx: float,
    cy: float,
    rx: float = HEAD_RX,
    ry: float = HEAD_RY,
    angle_deg: float = HEAD_ANGLE,
    shear: float = NOTE_SHEAR,
    soft: float = 4.5,
) -> np.ndarray:
    xr, yr = rotate_xy(cx, cy, angle_deg)
    xr = xr + yr * shear
    rad = np.sqrt((xr / max(rx, 1.0)) ** 2 + (yr / max(ry, 1.0)) ** 2)
    edge = soft / max(min(rx, ry), 1.0)
    return smoothstep(1.0 + edge, 1.0 - edge, rad)


def air_notehead_ring(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    width: float,
    angle_deg: float = HEAD_ANGLE,
    shear: float = NOTE_SHEAR,
    soft: float = 4.0,
) -> np.ndarray:
    outer = air_notehead(cx, cy, rx, ry, angle_deg, shear, soft)
    inner = air_notehead(cx, cy, max(rx - width, 10.0), max(ry - width * 0.72, 8.0), angle_deg, shear, soft)
    return clamp01(outer - inner * 0.98)


def air_ellipse_ring(
    cx: float, cy: float, rx: float, ry: float, width: float, angle_deg: float = 0.0, soft: float = 5.0
) -> np.ndarray:
    outer = air_ellipse(cx, cy, rx, ry, angle_deg, soft)
    inner = air_ellipse(cx, cy, max(rx - width, 8.0), max(ry - width, 6.0), angle_deg, soft)
    return clamp01(outer - inner * 0.96)


def air_ring(cx: float, cy: float, radius: float, width: float, soft: float = 6.0) -> np.ndarray:
    dist = np.sqrt((XX - cx) ** 2 + (YY - cy) ** 2)
    inner = radius - width * 0.5
    outer = radius + width * 0.5
    return smoothstep(inner - soft, inner + soft, dist) * smoothstep(outer + soft, outer - soft, dist)


def dist_segment(x0: float, y0: float, x1: float, y1: float) -> np.ndarray:
    vx, vy = x1 - x0, y1 - y0
    length = vx * vx + vy * vy + 1e-6
    t = clamp01(((XX - x0) * vx + (YY - y0) * vy) / length)
    px = x0 + t * vx
    py = y0 + t * vy
    return np.sqrt((XX - px) ** 2 + (YY - py) ** 2)


def air_capsule(x0: float, y0: float, x1: float, y1: float, radius: float, soft: float = 6.0) -> np.ndarray:
    return smoothstep(radius + soft, radius - soft, dist_segment(x0, y0, x1, y1))


def chrome_on(alpha: np.ndarray, cx: float, cy: float, rx: float, ry: float, albedo: np.ndarray) -> np.ndarray:
    nx = (XX - cx) / max(rx, 1.0)
    ny = (YY - cy) / max(ry, 1.0)
    r2 = nx * nx + ny * ny
    nz = np.sqrt(np.maximum(0.0, 1.0 - r2))
    key = nx * 0.52 + ny * -0.38 + nz * 0.76
    key = clamp01(key)
    spec = np.power(key, 16.0)
    rim = np.power(np.clip(1.0 - nz, 0.0, 1.0), 1.6)
    fill = clamp01(-ny) * 0.22
    color = albedo * (0.22 + 0.82 * key)[..., None]
    color = color + spec[..., None] * np.array([1.0, 0.96, 0.86], dtype=np.float32)
    color = color + rim[..., None] * albedo * 0.18
    color = color + fill[..., None] * np.array([0.88, 0.18, 0.58], dtype=np.float32)
    lit = np.zeros((H, W, 4), dtype=np.float32)
    a = clamp01(alpha)
    lit[..., :3] = np.clip(color, 0.0, 1.0)
    lit[..., 3] = a
    return lit


def chrome_ellipse(
    alpha: np.ndarray, cx: float, cy: float, rx: float, ry: float, angle_deg: float, albedo: np.ndarray
) -> np.ndarray:
    xr, yr = rotate_xy(cx, cy, angle_deg)
    nx = xr / max(rx, 1.0)
    ny = yr / max(ry, 1.0)
    r2 = nx * nx + ny * ny
    nz = np.sqrt(np.maximum(0.0, 1.0 - r2))
    ang = math.radians(angle_deg)
    cos_a, sin_a = math.cos(ang), math.sin(ang)
    sx = nx * cos_a - ny * sin_a
    sy = nx * sin_a + ny * cos_a
    key = clamp01(sx * 0.52 + sy * -0.38 + nz * 0.76)
    spec = np.power(key, 16.0)
    rim = np.power(np.clip(1.0 - nz, 0.0, 1.0), 1.6)
    fill = clamp01(-sy) * 0.22
    color = albedo * (0.22 + 0.82 * key)[..., None]
    color = color + spec[..., None] * np.array([1.0, 0.96, 0.86], dtype=np.float32)
    color = color + rim[..., None] * albedo * 0.18
    color = color + fill[..., None] * np.array([0.88, 0.18, 0.58], dtype=np.float32)
    lit = np.zeros((H, W, 4), dtype=np.float32)
    a = clamp01(alpha)
    lit[..., :3] = np.clip(color, 0.0, 1.0)
    lit[..., 3] = a
    return lit


def air_polyline(pts: list[tuple[float, float]], radius: float, soft: float = 4.0) -> np.ndarray:
    acc = np.zeros((H, W), dtype=np.float32)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        acc = np.maximum(acc, air_capsule(x0, y0, x1, y1, radius, soft))
    return acc


def stamp_staff(canvas: np.ndarray, color: np.ndarray, alpha: float) -> None:
    for i in range(5):
        y = 248.0 + i * 28.0
        line = smoothstep(2.4, 0.15, np.abs(YY - y)) * smoothstep(36.0, 64.0, XX) * smoothstep(476.0, 448.0, XX)
        stamp(canvas, color, line * alpha)


def beat(frame: int) -> tuple[float, float]:
    t = frame / FRAMES
    dy = -abs(math.sin(t * math.pi * 2.0)) * 14.0
    dx = math.sin(t * math.pi * 2.0) * 5.5
    return dx, dy


def pulse(frame: int, amp: float = 8.0, phase: float = 0.0) -> float:
    return math.sin(frame / FRAMES * math.pi * 2.0 + phase) * amp


def paint_venue(kind: str, frame: int) -> Image.Image:
    canvas = blank()
    if kind == "sunset":
        y = YY / (H - 1)
        sky = np.zeros((H, W, 3), dtype=np.float32)
        sky += (1.0 - y)[..., None] * np.array([0.98, 0.42, 0.18], dtype=np.float32)
        sky += y[..., None] * np.array([0.42, 0.08, 0.48], dtype=np.float32)
        mid = smoothstep(0.28, 0.62, y)
        sky = sky * (1.0 - mid)[..., None] + np.array([0.92, 0.22, 0.55], dtype=np.float32) * mid[..., None]
        stamp(canvas, sky, np.ones((H, W), dtype=np.float32))
        sun = air_disc(128.0, 118.0, 78.0, 28.0)
        glow = air_disc(128.0, 118.0, 130.0, 70.0)
        stamp(canvas, np.array([1.0, 0.82, 0.28], dtype=np.float32), glow * 0.45)
        stamp(canvas, np.array([1.0, 0.94, 0.62], dtype=np.float32), sun)
    elif kind == "lava":
        stamp(canvas, np.array([0.10, 0.04, 0.16], dtype=np.float32), np.ones((H, W), dtype=np.float32))
        blobs = (
            (140.0, 160.0, 78.0, (0.92, 0.18, 0.58), 0.4),
            (360.0, 240.0, 92.0, (0.18, 0.82, 0.78), 1.1),
            (250.0, 380.0, 110.0, (0.98, 0.55, 0.12), 2.2),
            (90.0, 360.0, 64.0, (0.72, 0.22, 0.92), 3.0),
            (420.0, 90.0, 54.0, (0.98, 0.32, 0.48), 1.7),
        )
        for i, (bx, by, br, col, phase) in enumerate(blobs):
            ox = pulse(frame, 18.0, phase)
            oy = pulse(frame, 12.0, phase + 1.2)
            blob = air_disc(bx + ox, by + oy, br, 36.0)
            stamp(canvas, np.array(col, dtype=np.float32), blob * (0.55 + 0.08 * (i % 3)))
    elif kind == "checker":
        stamp(canvas, np.array([0.12, 0.05, 0.18], dtype=np.float32), np.ones((H, W), dtype=np.float32))
        floor = YY > 250
        persp = np.maximum((YY - 250.0) / 180.0, 0.08)
        u = (XX - 256.0) / (persp * 90.0 + 8.0)
        v = (YY - 250.0) / (persp * 28.0 + 6.0)
        cells = (np.floor(u) + np.floor(v)) % 2
        gold = np.array([0.98, 0.78, 0.22], dtype=np.float32)
        mag = np.array([0.62, 0.08, 0.42], dtype=np.float32)
        tile = np.where(cells[..., None] > 0.5, gold, mag)
        fade = smoothstep(250.0, 290.0, YY) * smoothstep(510.0, 430.0, YY)
        stamp(canvas, tile, fade * floor.astype(np.float32))
        haze = air_disc(256.0, 210.0, 180.0, 90.0)
        stamp(canvas, np.array([0.95, 0.28, 0.62], dtype=np.float32), haze * 0.28)
    elif kind == "velvet":
        y = YY / (H - 1)
        wash = np.array([0.22, 0.04, 0.16], dtype=np.float32) * (1.0 - y)[..., None]
        wash = wash + np.array([0.08, 0.02, 0.10], dtype=np.float32) * y[..., None]
        stamp(canvas, wash, np.ones((H, W), dtype=np.float32))
        spot = air_disc(256.0, 200.0, 150.0, 110.0)
        stamp(canvas, np.array([0.72, 0.12, 0.32], dtype=np.float32), spot * 0.55)
        vignette = 1.0 - air_disc(256.0, 256.0, 280.0, 90.0)
        stamp(canvas, np.array([0.02, 0.0, 0.04], dtype=np.float32), vignette * 0.55)
    elif kind == "blacklight":
        stamp(canvas, np.array([0.04, 0.08, 0.14], dtype=np.float32), np.ones((H, W), dtype=np.float32))
        rng = np.random.default_rng(88)
        for i in range(18):
            px = float(40 + (i * 97) % 430)
            py = float(50 + (i * 53) % 410)
            pr = 10.0 + (i % 5) * 6.0
            glow = air_disc(px, py + pulse(frame, 6.0, i * 0.4), pr, 14.0)
            neon = np.array([0.35, 0.95, 0.55], dtype=np.float32) if i % 2 else np.array([0.85, 0.25, 0.95], dtype=np.float32)
            stamp(canvas, neon, glow * 0.7)
        _ = rng
    else:
        rad = np.sqrt((XX - 256.0) ** 2 + (YY - 220.0) ** 2) / 320.0
        metal = np.array([0.62, 0.68, 0.78], dtype=np.float32) * (1.0 - rad)[..., None]
        metal = metal + np.array([0.16, 0.18, 0.28], dtype=np.float32) * rad[..., None]
        highlight = air_disc(180.0, 120.0, 90.0, 70.0)
        stamp(canvas, metal, np.ones((H, W), dtype=np.float32))
        stamp(canvas, np.array([0.92, 0.95, 1.0], dtype=np.float32), highlight * 0.35)
    if kind == "sunset":
        stamp_staff(canvas, np.array([0.22, 0.06, 0.12], dtype=np.float32), 0.32)
    elif kind == "checker":
        stamp_staff(canvas, np.array([1.0, 0.92, 0.72], dtype=np.float32), 0.18)
    else:
        stamp_staff(canvas, np.array([1.0, 0.94, 0.82], dtype=np.float32), 0.28)
    return to_image(canvas)


def stem_points(dx: float, dy: float, hx: float | None = None, hy: float | None = None) -> tuple[float, float, float, float]:
    hx = CX + dx if hx is None else hx
    hy = HEAD_Y + dy if hy is None else hy
    ang = math.radians(HEAD_ANGLE)
    sx = hx + (HEAD_RX * 0.82) * math.cos(ang) + (HEAD_RY * NOTE_SHEAR * 0.35)
    sy = hy + (HEAD_RX * 0.55) * math.sin(ang)
    top_x = sx + 2.0
    top_y = sy - STEM_LEN
    return sx, sy, top_x, top_y


def layer_on(canvas: np.ndarray, piece: np.ndarray) -> None:
    stamp(canvas, piece[..., :3], piece[..., 3])


def paint_note(kind: str, frame: int) -> Image.Image:
    canvas = blank()
    dx, dy = beat(frame)
    albedo = METAL[kind]
    hx, hy = CX + dx, HEAD_Y + dy

    def notehead(cx: float, cy: float, rx: float, ry: float, hollow: bool = False) -> None:
        if hollow:
            ring = air_notehead_ring(cx, cy, rx, ry, 16.0)
            layer_on(canvas, chrome_ellipse(ring, cx, cy, rx, ry, HEAD_ANGLE, albedo))
        else:
            head = air_notehead(cx, cy, rx, ry)
            layer_on(canvas, chrome_ellipse(head, cx, cy, rx, ry, HEAD_ANGLE, albedo))

    def stem(attach_x: float, attach_y: float, top_x: float, top_y: float) -> None:
        body = air_capsule(attach_x, attach_y, top_x, top_y, STEM_W, 2.4)
        mx, my = (attach_x + top_x) * 0.5, (attach_y + top_y) * 0.5
        layer_on(canvas, chrome_on(body, mx, my, 16.0, STEM_LEN * 0.5, albedo * 0.94))

    def flag(top_x: float, top_y: float) -> None:
        pts = [
            (top_x + 1.0, top_y + 2.0),
            (top_x + 22.0, top_y + 8.0),
            (top_x + 74.0, top_y + 18.0),
            (top_x + 86.0, top_y + 48.0),
            (top_x + 62.0, top_y + 86.0),
            (top_x + 28.0, top_y + 74.0),
            (top_x + 8.0, top_y + 42.0),
        ]
        hook = air_polyline(pts, 8.0, 3.2)
        fill = air_polyline(
            [
                (top_x + 4.0, top_y + 10.0),
                (top_x + 68.0, top_y + 24.0),
                (top_x + 70.0, top_y + 52.0),
                (top_x + 22.0, top_y + 58.0),
            ],
            16.0,
            5.0,
        )
        banner = clamp01(hook + fill * 0.9)
        layer_on(canvas, chrome_on(banner, top_x + 42.0, top_y + 40.0, 48.0, 42.0, albedo))

    if kind == "whole":
        notehead(hx, hy, HEAD_RX * 1.12, HEAD_RY * 1.18, hollow=True)
        return to_image(canvas)

    notehead(hx, hy, HEAD_RX, HEAD_RY)
    sx, sy, tx, ty = stem_points(dx, dy, hx, hy)
    stem(sx, sy, tx, ty)

    if kind == "eighth":
        flag(tx, ty)

    if kind == "beamed":
        hx2, hy2 = hx + 128.0, hy + 18.0
        notehead(hx2, hy2, HEAD_RX * 0.92, HEAD_RY * 0.92)
        sx2, sy2, tx2, ty2 = stem_points(dx, dy, hx2, hy2)
        stem(sx2, sy2, tx2, ty2)
        beam = air_capsule(tx - 1.0, ty + 8.0, tx2 + 1.0, ty2 + 8.0, 12.0, 2.8)
        beam2 = air_capsule(tx - 1.0, ty + 32.0, tx2 + 1.0, ty2 + 32.0, 9.0, 2.6)
        layer_on(canvas, chrome_on(clamp01(beam + beam2), (tx + tx2) * 0.5, ty + 18.0, 78.0, 24.0, albedo))

    return to_image(canvas)


def paint_expression(kind: str, frame: int) -> Image.Image:
    canvas = blank()
    dx, dy = beat(frame)
    hx, hy = CX + dx, HEAD_Y + dy
    blink = frame in (5, 6)
    lx, rx = hx - 26.0, hx + 26.0
    ey = hy - 4.0

    def eye(x: float, y: float, shut: bool, starry: bool = False) -> None:
        if shut:
            lid = air_capsule(x - 16.0, y, x + 16.0, y + 2.0, 4.0, 2.0)
            stamp(canvas, np.array([0.12, 0.04, 0.10], dtype=np.float32), lid)
            return
        white = air_disc(x, y, 16.0, 3.0)
        stamp(canvas, np.array([0.08, 0.04, 0.10], dtype=np.float32), white)
        if starry:
            spark = air_disc(x, y, 7.0, 2.0)
            arm = air_capsule(x - 10.0, y, x + 10.0, y, 2.4, 1.5) + air_capsule(x, y - 10.0, x, y + 10.0, 2.4, 1.5)
            stamp(canvas, np.array([1.0, 0.86, 0.35], dtype=np.float32), clamp01(spark + arm * 0.85))
        else:
            pupil = air_disc(x + 2.0, y + 1.0, 7.5, 2.0)
            glint = air_disc(x - 4.0, y - 5.0, 3.2, 1.4)
            stamp(canvas, np.array([0.98, 0.55, 0.18], dtype=np.float32), pupil)
            stamp(canvas, np.array([1.0, 1.0, 0.95], dtype=np.float32), glint)

    if kind == "cool":
        eye(lx, ey + 4.0, blink)
        eye(rx, ey + 4.0, blink)
        brow = air_capsule(lx - 18.0, ey - 16.0, lx + 12.0, ey - 10.0, 3.2, 1.8)
        brow2 = air_capsule(rx - 12.0, ey - 10.0, rx + 18.0, ey - 16.0, 3.2, 1.8)
        stamp(canvas, np.array([0.12, 0.04, 0.10], dtype=np.float32), clamp01(brow + brow2))
        mouth = air_capsule(hx - 18.0, hy + 22.0, hx + 18.0, hy + 20.0, 3.2, 1.8)
        stamp(canvas, np.array([0.18, 0.04, 0.10], dtype=np.float32), mouth)
    elif kind == "shout":
        eye(lx, ey - 4.0, blink)
        eye(rx, ey - 4.0, blink)
        mouth = air_disc(hx, hy + 24.0, 16.0, 4.0)
        hole = air_disc(hx, hy + 24.0, 9.0, 3.0)
        stamp(canvas, np.array([0.55, 0.08, 0.22], dtype=np.float32), mouth)
        stamp(canvas, np.array([0.12, 0.02, 0.08], dtype=np.float32), hole)
    elif kind == "wink":
        eye(lx, ey, True)
        eye(rx, ey, blink)
        mouth = air_disc(hx + 6.0, hy + 20.0, 9.0, 3.0)
        stamp(canvas, np.array([0.85, 0.22, 0.45], dtype=np.float32), mouth)
    elif kind == "groove":
        eye(lx, ey + 2.0, True)
        eye(rx, ey + 2.0, True)
        smile = air_ring(hx, hy + 10.0, 24.0, 7.0, 3.0) * (YY > hy + 8.0)
        stamp(canvas, np.array([0.18, 0.05, 0.12], dtype=np.float32), smile)
    else:
        eye(lx, ey, blink, starry=True)
        eye(rx, ey, blink, starry=True)
        mouth = air_disc(hx, hy + 20.0, 7.0, 3.0)
        stamp(canvas, np.array([0.95, 0.35, 0.55], dtype=np.float32), mouth)
    return to_image(canvas)


def paint_topper(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return to_image(blank())
    canvas = blank()
    dx, dy = beat(frame)
    hx, hy = CX + dx, HEAD_Y + dy
    if kind == "afro":
        puff = air_notehead(hx, hy - 4.0, HEAD_RX + 22.0, HEAD_RY + 26.0, soft=8.0)
        inner = air_notehead(hx, hy + 2.0, HEAD_RX * 0.98, HEAD_RY * 0.98, soft=3.5)
        afro = clamp01(puff - inner)
        gold = np.array([0.42, 0.18, 0.08], dtype=np.float32)
        stamp(canvas, gold, afro)
        sheen = air_disc(hx - 34.0, hy - 40.0, 22.0, 12.0)
        stamp(canvas, np.array([0.85, 0.48, 0.18], dtype=np.float32), sheen * afro)
    elif kind == "shades":
        left = air_capsule(hx - 48.0, hy - 4.0, hx - 6.0, hy - 2.0, 12.0, 3.5)
        right = air_capsule(hx + 6.0, hy - 2.0, hx + 48.0, hy - 4.0, 12.0, 3.5)
        bridge = air_capsule(hx - 8.0, hy - 4.0, hx + 8.0, hy - 4.0, 3.2, 1.6)
        dark = np.array([0.06, 0.04, 0.08], dtype=np.float32)
        stamp(canvas, dark, clamp01(left + right + bridge))
        glint = air_capsule(hx - 36.0, hy - 10.0, hx - 20.0, hy - 6.0, 2.0, 1.2)
        stamp(canvas, np.array([1.0, 0.9, 0.55], dtype=np.float32), glint)
    elif kind == "visor":
        brim = air_capsule(hx - 64.0, hy - 36.0, hx + 36.0, hy - 32.0, 10.0, 4.5)
        cap = air_ellipse(hx, hy - 38.0, 58.0, 28.0, -8.0, 7.0) * (YY < hy - 18.0)
        visor = np.array([0.18, 0.82, 0.62], dtype=np.float32)
        stamp(canvas, visor * 0.55, cap)
        layer_on(canvas, chrome_on(brim, hx - 10.0, hy - 34.0, 56.0, 14.0, visor))
    else:
        ring = air_ellipse_ring(hx, hy - 58.0, 46.0, 18.0, 9.0, -8.0, 4.0)
        glow = air_ellipse(hx, hy - 58.0, 54.0, 24.0, -8.0, 16.0)
        stamp(canvas, np.array([1.0, 0.86, 0.35], dtype=np.float32), glow * 0.32)
        layer_on(canvas, chrome_ellipse(ring, hx, hy - 58.0, 46.0, 18.0, -8.0, np.array([1.0, 0.84, 0.28], dtype=np.float32)))
    return to_image(canvas)


def paint_cable(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return to_image(blank())
    canvas = blank()
    dx, dy = beat(frame)
    hx, hy = CX + dx, HEAD_Y + dy
    sx, sy, tx, ty = stem_points(dx, dy)
    if kind == "chain":
        gold = np.array([0.98, 0.78, 0.22], dtype=np.float32)
        for i, t in enumerate(np.linspace(0.12, 0.88, 6)):
            px = hx - 30.0 + 60.0 * t
            py = hy + HEAD_RY * 0.62 + math.sin(t * math.pi) * 7.0
            link = air_ring(px, py, 8.5, 3.8, 1.8)
            layer_on(canvas, chrome_on(link, px, py, 9.0, 9.0, gold))
    elif kind == "cans":
        band = air_capsule(hx - 72.0, hy - 16.0, hx + 72.0, hy - 16.0, 5.5, 3.0)
        left = air_disc(hx - 76.0, hy + 2.0, 22.0, 5.0)
        right = air_disc(hx + 76.0, hy + 2.0, 22.0, 5.0)
        chrome = np.array([0.82, 0.86, 0.95], dtype=np.float32)
        layer_on(canvas, chrome_on(band, hx, hy - 16.0, 76.0, 10.0, chrome))
        layer_on(canvas, chrome_on(left, hx - 76.0, hy + 2.0, 22.0, 22.0, chrome))
        layer_on(canvas, chrome_on(right, hx + 76.0, hy + 2.0, 22.0, 22.0, chrome))
        pad = np.array([0.18, 0.06, 0.12], dtype=np.float32)
        stamp(canvas, pad, air_disc(hx - 76.0, hy + 2.0, 11.0, 3.0))
        stamp(canvas, pad, air_disc(hx + 76.0, hy + 2.0, 11.0, 3.0))
    else:
        stick = air_capsule(hx - 96.0, hy - 8.0, hx - 128.0, hy + 72.0, 5.0, 3.0)
        ball = air_disc(hx - 96.0, hy - 10.0, 18.0, 5.0)
        mesh = air_disc(hx - 96.0, hy - 10.0, 11.0, 3.0)
        silver = np.array([0.78, 0.82, 0.9], dtype=np.float32)
        layer_on(canvas, chrome_on(stick, hx - 112.0, hy + 32.0, 12.0, 46.0, silver))
        layer_on(canvas, chrome_on(ball, hx - 96.0, hy - 10.0, 18.0, 18.0, silver))
        stamp(canvas, np.array([0.12, 0.1, 0.14], dtype=np.float32), mesh)
    return to_image(canvas)


def paint_riff(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return to_image(blank())
    canvas = blank()
    ox = pulse(frame, 10.0, 0.6)
    oy = pulse(frame, 12.0, 1.8)
    if kind == "treble":
        gold = np.array([0.98, 0.82, 0.28], dtype=np.float32)
        x, y = 86.0 + ox, 118.0 + oy
        s = air_capsule(x, y - 50.0, x + 18.0, y - 10.0, 7.0, 3.0)
        s2 = air_capsule(x + 18.0, y - 10.0, x - 8.0, y + 28.0, 7.0, 3.0)
        s3 = air_capsule(x - 8.0, y + 28.0, x + 22.0, y + 58.0, 7.0, 3.0)
        dot = air_disc(x + 6.0, y + 70.0, 10.0, 3.0)
        for piece, px, py, rx, ry in (
            (s, x + 9.0, y - 30.0, 20.0, 24.0),
            (s2, x + 5.0, y + 8.0, 20.0, 24.0),
            (s3, x + 7.0, y + 42.0, 20.0, 24.0),
            (dot, x + 6.0, y + 70.0, 10.0, 10.0),
        ):
            layer_on(canvas, chrome_on(piece, px, py, rx, ry, gold))
    elif kind == "vinyl":
        x, y = 86.0 + ox * 0.4, 92.0 + oy * 0.3
        disc = air_disc(x, y, 48.0, 6.0)
        groove = air_ring(x, y, 32.0, 3.0, 2.0) + air_ring(x, y, 22.0, 3.0, 2.0)
        hole = air_disc(x, y, 8.0, 2.0)
        stamp(canvas, np.array([0.08, 0.06, 0.10], dtype=np.float32), disc)
        stamp(canvas, np.array([0.35, 0.32, 0.38], dtype=np.float32), groove)
        stamp(canvas, np.array([0.95, 0.28, 0.55], dtype=np.float32), hole)
    elif kind == "stars":
        gold = np.array([1.0, 0.88, 0.38], dtype=np.float32)
        for i, (x, y) in enumerate(((72.0, 92.0), (430.0, 70.0), (448.0, 210.0), (64.0, 250.0))):
            s = 0.65 + 0.35 * abs(math.sin(frame / FRAMES * math.pi * 2.0 + i))
            cx, cy, r = x + ox * 0.3, y + oy * 0.3, 10.0 * s
            burst = air_disc(cx, cy, r, 4.0)
            burst = burst + air_capsule(cx - r * 1.8, cy, cx + r * 1.8, cy, 2.2, 1.4)
            burst = burst + air_capsule(cx, cy - r * 1.8, cx, cy + r * 1.8, 2.2, 1.4)
            stamp(canvas, gold, clamp01(burst) * (0.7 + 0.3 * s))
    else:
        x, y = 78.0 + ox, 200.0 + oy
        bolt = (
            air_capsule(x, y - 36.0, x + 18.0, y - 8.0, 6.0, 3.0)
            + air_capsule(x + 18.0, y - 8.0, x - 10.0, y + 8.0, 6.0, 3.0)
            + air_capsule(x - 10.0, y + 8.0, x + 16.0, y + 40.0, 6.0, 3.0)
        )
        layer_on(
            canvas,
            chrome_on(clamp01(bolt), x + 4.0, y, 28.0, 44.0, np.array([1.0, 0.86, 0.22], dtype=np.float32)),
        )
    return to_image(canvas)


TRAIT_SPEC: dict[str, list[tuple[str, str, int]]] = {
    "venue": [
        ("sunset", "Sunset Strip", 24),
        ("lava", "Lava Lamp", 20),
        ("checker", "Disco Floor", 18),
        ("velvet", "Velvet Night", 16),
        ("blacklight", "Blacklight", 12),
        ("chrome", "Chrome Wash", 10),
    ],
    "note": [
        ("quarter", "Quarter", 34),
        ("eighth", "Eighth", 28),
        ("whole", "Whole", 22),
        ("beamed", "Beamed", 16),
    ],
    "expression": [
        ("cool", "Cool", 26),
        ("shout", "Shout", 20),
        ("wink", "Wink", 18),
        ("groove", "Groove", 20),
        ("star", "Starry", 16),
    ],
    "topper": [
        ("none", "None", 28),
        ("afro", "Afro", 20),
        ("shades", "Shades", 22),
        ("visor", "Visor", 16),
        ("halo", "Halo", 14),
    ],
    "cable": [
        ("none", "None", 36),
        ("chain", "Gold Chain", 24),
        ("cans", "Cans", 22),
        ("mic", "Mic", 18),
    ],
    "riff": [
        ("none", "None", 32),
        ("treble", "Treble", 20),
        ("vinyl", "Vinyl", 18),
        ("stars", "Stars", 16),
        ("bolt", "Bolt", 14),
    ],
}

PAINTERS = {
    "venue": {k: (lambda kind: (lambda frame, k=kind: paint_venue(k, frame)))(k) for k in VENUES},
    "note": {k: (lambda kind: (lambda frame, k=kind: paint_note(k, frame)))(k) for k in NOTES},
    "expression": {k: (lambda kind: (lambda frame, k=kind: paint_expression(k, frame)))(k) for k in EXPRESSIONS},
    "topper": {k: (lambda kind: (lambda frame, k=kind: paint_topper(k, frame)))(k) for k in TOPPERS},
    "cable": {k: (lambda kind: (lambda frame, k=kind: paint_cable(k, frame)))(k) for k in CABLES},
    "riff": {k: (lambda kind: (lambda frame, k=kind: paint_riff(k, frame)))(k) for k in RIFFS},
}

STACK = ("venue", "note", "expression", "topper", "cable", "riff")

SIGNATURES = [
    {"venue": "sunset", "note": "eighth", "expression": "cool", "topper": "shades", "cable": "chain", "riff": "vinyl"},
    {"venue": "lava", "note": "quarter", "expression": "shout", "topper": "afro", "cable": "cans", "riff": "treble"},
    {"venue": "checker", "note": "beamed", "expression": "wink", "topper": "visor", "cable": "mic", "riff": "stars"},
    {"venue": "velvet", "note": "whole", "expression": "groove", "topper": "halo", "cable": "none", "riff": "bolt"},
    {"venue": "blacklight", "note": "eighth", "expression": "star", "topper": "afro", "cable": "chain", "riff": "none"},
    {"venue": "chrome", "note": "quarter", "expression": "cool", "topper": "shades", "cable": "mic", "riff": "treble"},
    {"venue": "sunset", "note": "whole", "expression": "wink", "topper": "none", "cable": "cans", "riff": "stars"},
    {"venue": "lava", "note": "beamed", "expression": "groove", "topper": "halo", "cable": "chain", "riff": "vinyl"},
    {"venue": "checker", "note": "eighth", "expression": "shout", "topper": "none", "cable": "none", "riff": "bolt"},
    {"venue": "velvet", "note": "quarter", "expression": "star", "topper": "visor", "cable": "cans", "riff": "none"},
    {"venue": "blacklight", "note": "whole", "expression": "cool", "topper": "shades", "cable": "mic", "riff": "treble"},
    {"venue": "chrome", "note": "beamed", "expression": "shout", "topper": "afro", "cable": "none", "riff": "stars"},
    {"venue": "sunset", "note": "quarter", "expression": "groove", "topper": "halo", "cable": "chain", "riff": "bolt"},
    {"venue": "lava", "note": "eighth", "expression": "wink", "topper": "visor", "cable": "cans", "riff": "vinyl"},
    {"venue": "checker", "note": "whole", "expression": "star", "topper": "afro", "cable": "none", "riff": "treble"},
    {"venue": "velvet", "note": "beamed", "expression": "cool", "topper": "shades", "cable": "mic", "riff": "stars"},
]

TRAIT_LABELS = (
    ("venue", "Venue"),
    ("note", "Note"),
    ("expression", "Expression"),
    ("topper", "Topper"),
    ("cable", "Cable"),
    ("riff", "Riff"),
)

COLLECTION_DESCRIPTION = (
    "Groovy Nation is an 8,888-piece collection of looping musical-note PFP GIFs. "
    "Each citizen is stacked from six layers — venue, note, expression, topper, cable, and riff — "
    "then flattened onto one 12-frame GIF. Real notation silhouettes: tilted oval heads, thin stems, flags and beams at the top."
)

COLLECTION_STORY = (
    "Welcome to Groovy Nation.\n\n"
    "An 8,888-piece collection of looping musical-note PFP GIFs on Robinhood Chain. "
    "Each citizen is stacked from six layers — venue, note, expression, topper, cable, and riff — "
    "then flattened onto one 12-frame GIF. Tilted oval noteheads. Thin stems going up. Flags and beams at the top. Lava-lamp stages.\n\n"
    "Four notes only: quarter, eighth, whole, and beamed. The drawing stays airbrushed chrome on real notation — "
    "not a sphere with a stick. Shades sit on the head. Chains hang on the stem. "
    "Riffs float beside the beat. One shared clock.\n\n"
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
        "name": "Groovy Nation",
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Four notation bodies share one bounce; toppers, cables, and riffs never edit the note.",
    }
    (TRAIT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def build_samples() -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    samples = []
    for index, selection in enumerate(SIGNATURES, start=1):
        print(f"  sample #{index}")
        frames = compose_selection(selection)
        save_loop_gif(frames, PREVIEW_DIR / f"{index}.gif", DURATION_MS, colors=64)
        samples.append(
            {
                "id": index,
                "name": f"Groovy #{index}",
                "image": f"/groovy-preview/{index}.gif",
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
                f'    image: "{sample["image"]}?v=2",\n'
            f"    attributes: [\n      {attrs},\n    ],\n"
            "  }"
        )
    (SRC_DATA / "groovy-gallery.ts").write_text(
        "export type GroovySample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const groovySamples: GroovySample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array(
        [
            [0.98, 0.42, 0.18],
            [0.92, 0.22, 0.55],
            [0.42, 0.08, 0.48],
            [0.12, 0.05, 0.18],
        ],
        dtype=np.float32,
    )
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)
    y = np.linspace(0.0, 1.0, height, dtype=np.float32)
    xx, yy = np.meshgrid(x, y)
    t = np.clip(xx * 0.62 + yy * 0.38, 0.0, 0.999) * (len(colors) - 1)
    i0 = np.floor(t).astype(np.int32)
    f = (t - i0)[..., None]
    c0 = colors[i0]
    c1 = colors[np.clip(i0 + 1, 0, len(colors) - 1)]
    rgb_out = c0 * (1.0 - f) + c1 * f
    arr = np.dstack([np.clip(rgb_out * 255.0, 0, 255).astype(np.uint8), np.full((height, width), 255, dtype=np.uint8)])
    return Image.fromarray(arr, "RGBA")


def write_collection_meta() -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    (META_DIR / "groovy-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / "groovy.json").write_text(
        json.dumps(
            {
                "name": "Groovy Nation",
                "symbol": "GROOVY",
                "description": COLLECTION_DESCRIPTION,
                "image": "/brand/collection-groovy.gif",
                "featured_image": "/brand/featured-groovy.jpg",
                "banner_image": "/brand/banner-groovy.png",
                "opensea_banner_image": "/brand/banner-groovy-opensea.jpg",
                "external_link": "/groovy",
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
    ImageDraw.Draw(mask).ellipse((18, 18, SIZE - 18, SIZE - 18), fill=255)
    logo.putalpha(Image.composite(logo.split()[-1], Image.new("L", (SIZE, SIZE), 0), mask))
    ring = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((10, 10, SIZE - 10, SIZE - 10), outline=(255, 196, 64, 255), width=10)
    logo = Image.alpha_composite(logo, ring)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / "logo-groovy.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / "logo-groovy-loop.png",
    )

    def lineup(width: int, height: int, faces: list[Image.Image]) -> Image.Image:
        canvas = panoramic_wash(width, height)
        count = len(faces)
        size = int(height * 0.82)
        overlap = size // 5
        total = size * count - overlap * (count - 1)
        start_x = (width - total) // 2
        y = (height - size) // 2 + int(height * 0.04)
        for index, portrait in enumerate(faces):
            px = start_x + index * (size - overlap)
            place_portrait(canvas, portrait, px, y, size, radius=max(36, size // 10))
        return canvas

    save_image(lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / "banner-groovy.png", quality=94)
    save_image(lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / "banner-groovy-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=64)
    place_portrait(featured, portraits[3], 540, 130, 560, radius=64)
    save_image(featured.convert("RGB"), BRAND_DIR / "featured-groovy.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(gif_frames, BRAND_DIR / "collection-groovy.gif", DURATION_MS, colors=64)
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Groovy Nation brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Groovy Nation airbrush-note trait loops…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
