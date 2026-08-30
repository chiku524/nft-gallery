#!/usr/bin/env python3
"""Paint Afterimages — 12 unique 1:1 APNG paintings for an OpenSea Drop.

Each token is a finished looping painting, not a trait stack.
16 frames, 100ms, 640×640. Upload pack + site previews land together.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from gif_bake import save_loop_gif

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIR = ROOT / "public" / "afterimages"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
OUT = ROOT / "generated" / "afterimages"
IMAGE_DIR = OUT / "images"
GIF_DIR = OUT / "gifs"
JSON_DIR = OUT / "json"

SIZE = 640
FRAMES = 16
DURATION_MS = 100
H, W = SIZE, SIZE


def clamp01(x: np.ndarray | float) -> np.ndarray | float:
    return np.clip(x, 0.0, 1.0)


def smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = clamp01((x - edge0) / (edge1 - edge0))
    return t * t * (3.0 - 2.0 * t)


def rgb(hex_color: str) -> np.ndarray:
    value = hex_color.lstrip("#")
    return np.array([int(value[i : i + 2], 16) / 255.0 for i in (0, 2, 4)], dtype=np.float32)


def mix(a: np.ndarray | float, b: np.ndarray | float, t: float | np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    t = np.asarray(t, dtype=np.float32)
    if t.ndim >= 2 and a.ndim == 1:
        t = t[..., None]
    return a * (1.0 - t) + b * t


def blank() -> np.ndarray:
    return np.zeros((H, W, 4), dtype=np.float32)


def grid() -> tuple[np.ndarray, np.ndarray]:
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return xx, yy


def over(dst: np.ndarray, src: np.ndarray) -> None:
    sa = src[..., 3:4]
    da = dst[..., 3:4]
    out_a = sa + da * (1.0 - sa)
    rgb_out = src[..., :3] * sa + dst[..., :3] * da * (1.0 - sa)
    dst[..., :3] = np.divide(rgb_out, out_a, out=np.zeros_like(rgb_out), where=out_a > 1e-6)
    dst[..., 3:4] = out_a


def fill(dst: np.ndarray, color: np.ndarray, opacity: float = 1.0) -> None:
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = opacity
    over(dst, layer)


def vertical_wash(top: np.ndarray, bottom: np.ndarray, power: float = 1.0) -> np.ndarray:
    xx, yy = grid()
    t = (yy / (H - 1)) ** power
    dst = blank()
    dst[..., :3] = mix(top, bottom, t)
    dst[..., 3] = 1.0
    return dst


def glow(dst: np.ndarray, cx: float, cy: float, r: float, color: np.ndarray, opacity: float) -> None:
    xx, yy = grid()
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = np.exp(-0.5 * (d / max(r, 1.0)) ** 2) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def disc(
    dst: np.ndarray,
    cx: float,
    cy: float,
    r: float,
    color: np.ndarray,
    opacity: float = 1.0,
    soft: float = 2.0,
) -> None:
    xx, yy = grid()
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = smoothstep(r + soft, r - soft, d) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def ellipse(
    dst: np.ndarray,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    color: np.ndarray,
    opacity: float = 1.0,
    soft: float = 2.0,
) -> None:
    xx, yy = grid()
    d = np.sqrt(((xx - cx) / max(rx, 1.0)) ** 2 + ((yy - cy) / max(ry, 1.0)) ** 2)
    a = smoothstep(1.0 + soft / max(rx, ry), 1.0 - soft / max(rx, ry), d) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def rect(
    dst: np.ndarray,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    color: np.ndarray,
    opacity: float = 1.0,
    radius: float = 0.0,
) -> None:
    xx, yy = grid()
    if radius <= 0:
        mask = (xx >= x0) & (xx <= x1) & (yy >= y0) & (yy <= y1)
        layer = blank()
        layer[..., :3] = color
        layer[..., 3] = mask.astype(np.float32) * opacity
        over(dst, layer)
        return
    cx = np.clip(xx, x0 + radius, x1 - radius)
    cy = np.clip(yy, y0 + radius, y1 - radius)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    a = smoothstep(radius + 1.4, radius - 1.4, d) * opacity
    layer = blank()
    layer[..., :3] = color
    layer[..., 3] = a
    over(dst, layer)


def phase(frame: int) -> float:
    return 2.0 * math.pi * frame / FRAMES


def to_image(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(arr * 255.0, 0, 255).astype(np.uint8), "RGBA")


def save_apng(frames: list[Image.Image], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    stamped = []
    for index, frame in enumerate(frames):
        copy = frame.convert("RGBA")
        pixels = copy.load()
        r, g, b, a = pixels[0, 0]
        pixels[0, 0] = (r, g, b, max(a, 1) if a == 0 else a)
        pixels[1, 0] = (index, 0, FRAMES, 1)
        stamped.append(copy)
    stamped[0].save(
        path,
        save_all=True,
        append_images=stamped[1:],
        duration=[DURATION_MS] * len(stamped),
        loop=0,
        format="PNG",
        disposal=1,
        blend=0,
        compress_level=6,
    )


WORKS = [
    {
        "id": 1,
        "slug": "moonrise",
        "title": "Moonrise Over Still Water",
        "description": "A silver moon climbs a indigo inlet. The water holds the climb a beat later.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Indigo Silver",
            "Motion": "Rise",
            "Season": "Night",
            "Medium": "APNG",
        },
    },
    {
        "id": 2,
        "slug": "stained-glass",
        "title": "Stained Glass Breath",
        "description": "Jewel panes inhale gold. Lead lines hold while the colors keep changing their mind.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Jewel Gold",
            "Motion": "Pulse",
            "Season": "Dusk",
            "Medium": "APNG",
        },
    },
    {
        "id": 3,
        "slug": "petal-storm",
        "title": "Petal Storm",
        "description": "Blush petals fall through cream light and never quite land.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Blush Cream",
            "Motion": "Fall",
            "Season": "Spring",
            "Medium": "APNG",
        },
    },
    {
        "id": 4,
        "slug": "lighthouse",
        "title": "Lighthouse Sweep",
        "description": "An amber beam turns over navy water. Foam remembers the last pass.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Navy Amber",
            "Motion": "Sweep",
            "Season": "Night",
            "Medium": "APNG",
        },
    },
    {
        "id": 5,
        "slug": "coral-bloom",
        "title": "Coral Bloom",
        "description": "Anemones open under teal water. A gold fish threads the bloom.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Teal Salmon",
            "Motion": "Bloom",
            "Season": "Tide",
            "Medium": "APNG",
        },
    },
    {
        "id": 6,
        "slug": "neon-dusk",
        "title": "Neon Dusk",
        "description": "A city silhouette holds still while magenta and cyan signs keep arguing.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Magenta Cyan",
            "Motion": "Flicker",
            "Season": "Dusk",
            "Medium": "APNG",
        },
    },
    {
        "id": 7,
        "slug": "firefly-grove",
        "title": "Firefly Grove",
        "description": "Dark pines, a wet floor, and gold specks that refuse a single path.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Forest Gold",
            "Motion": "Drift",
            "Season": "Night",
            "Medium": "APNG",
        },
    },
    {
        "id": 8,
        "slug": "corona",
        "title": "Corona",
        "description": "A black disc covers the sun. The flare keeps finding new edges.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Black Gold",
            "Motion": "Flare",
            "Season": "Eclipse",
            "Medium": "APNG",
        },
    },
    {
        "id": 9,
        "slug": "koi-mirror",
        "title": "Koi Mirror",
        "description": "Orange and white koi turn under a jade surface. The pond is the painting.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Jade Orange",
            "Motion": "Orbit",
            "Season": "Garden",
            "Medium": "APNG",
        },
    },
    {
        "id": 10,
        "slug": "heat-shimmer",
        "title": "Heat Shimmer",
        "description": "Dunes wait. The air above them will not.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Ochre Sky",
            "Motion": "Shimmer",
            "Season": "Noon",
            "Medium": "APNG",
        },
    },
    {
        "id": 11,
        "slug": "ice-fracture",
        "title": "Ice Fracture",
        "description": "A frozen lake splits. Light travels the crack before the ice does.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Ice Navy",
            "Motion": "Crack",
            "Season": "Winter",
            "Medium": "APNG",
        },
    },
    {
        "id": 12,
        "slug": "nave-light",
        "title": "Nave Light",
        "description": "Stone holds. A honey shaft of dust keeps rewriting the aisle.",
        "attributes": {
            "Series": "Afterimages",
            "Palette": "Stone Honey",
            "Motion": "Motes",
            "Season": "Afternoon",
            "Medium": "APNG",
        },
    },
]


def paint_moonrise(frame: int) -> np.ndarray:
    t = phase(frame)
    moon_y = 168.0 - 22.0 * math.sin(t)
    dst = vertical_wash(rgb("#0b1028"), rgb("#1a2748"), 0.85)
    glow(dst, 320, moon_y, 140, rgb("#c9d7ff"), 0.28)
    disc(dst, 320, moon_y, 54, rgb("#f4f1ff"), 0.96, soft=3)
    disc(dst, 308, moon_y - 8, 16, rgb("#d7deef"), 0.35, soft=4)
    xx, yy = grid()
    horizon = 390.0 + 4.0 * np.sin(xx / 40.0 + t)
    water = blank()
    water[..., :3] = mix(rgb("#10243a"), rgb("#0a1628"), (yy - 390) / 250)
    water[..., 3] = smoothstep(horizon - 8, horizon + 4, yy)
    over(dst, water)
    for i in range(18):
        ripple_y = 430 + i * 12 + 3 * math.sin(t + i * 0.4)
        ellipse(dst, 320, ripple_y, 90 + i * 12, 5 + i * 0.4, rgb("#c9d7ff"), 0.07 + 0.02 * math.sin(t + i))
    glow(dst, 320, 430, 90, rgb("#e8eeff"), 0.18 + 0.06 * math.sin(t))
    return dst


def paint_stained_glass(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#1a1020"), rgb("#0d0a12"))
    rect(dst, 90, 40, 550, 600, rgb("#2a1c14"), 1.0, radius=18)
    panes = [
        (140, 90, 300, 250, "#7a1f4a"),
        (320, 90, 500, 250, "#1d4e89"),
        (140, 270, 300, 430, "#c9a227"),
        (320, 270, 500, 430, "#2f6b4f"),
        (140, 450, 300, 580, "#8b3d1b"),
        (320, 450, 500, 580, "#5c2d8a"),
    ]
    for i, (x0, y0, x1, y1, color) in enumerate(panes):
        pulse = 0.72 + 0.22 * math.sin(t + i * 0.9)
        rect(dst, x0, y0, x1, y1, rgb(color), pulse, radius=8)
        glow(dst, (x0 + x1) / 2, (y0 + y1) / 2, 70, rgb(color), 0.16 * pulse)
    for x in (140, 300, 320, 500):
        rect(dst, x - 6, 80, x + 6, 590, rgb("#3a2a1c"), 0.95)
    for y in (90, 250, 270, 430, 450, 580):
        rect(dst, 130, y - 6, 510, y + 6, rgb("#3a2a1c"), 0.95)
    glow(dst, 320, 300, 180, rgb("#f0d48a"), 0.12 + 0.08 * math.sin(t))
    return dst


def paint_petal_storm(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#f7e6d8"), rgb("#e8b8b0"), 0.7)
    glow(dst, 480, 90, 180, rgb("#fff6ea"), 0.45)
    disc(dst, 500, 70, 46, rgb("#fff4d8"), 0.9)
    rng = np.random.default_rng(31)
    for i in range(42):
        seed = rng.random(4)
        x = (seed[0] * W + 90 * math.sin(t + i) + 40 * i) % (W + 80) - 40
        y = (seed[1] * H + (frame * 18 + i * 21)) % (H + 60) - 30
        rot = 10 + 8 * math.sin(t + i)
        ellipse(dst, x, y, rot, rot * 0.45, mix(rgb("#e37a8a"), rgb("#f4c4b0"), seed[2]), 0.55 + 0.25 * seed[3])
    glow(dst, 200, 520, 160, rgb("#f0c8c0"), 0.2)
    return dst


def paint_lighthouse(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#07101f"), rgb("#15243a"))
    angle = t
    xx, yy = grid()
    beam_x = 430 + math.cos(angle) * 220
    beam_y = 250 + math.sin(angle) * 40
    glow(dst, beam_x, beam_y, 160, rgb("#f2c15a"), 0.22)
    # cliff
    cliff = blank()
    cliff_edge = 430 + 18 * np.sin(xx / 50.0)
    cliff[..., :3] = rgb("#1b2230")
    cliff[..., 3] = smoothstep(cliff_edge - 10, cliff_edge + 20, yy) * (xx < 280).astype(np.float32)
    over(dst, cliff)
    water = blank()
    water[..., :3] = mix(rgb("#10263d"), rgb("#08141f"), (yy - 420) / 220)
    water[..., 3] = smoothstep(470, 500, yy)
    over(dst, water)
    rect(dst, 168, 210, 232, 470, rgb("#d8d2c4"), 1.0, radius=6)
    rect(dst, 156, 188, 244, 230, rgb("#efe6d2"), 1.0, radius=8)
    glow(dst, 200, 208, 36, rgb("#ffe39a"), 0.7 + 0.2 * math.sin(t * 2))
    disc(dst, 200, 208, 10, rgb("#fff6d2"), 0.95)
    for i in range(10):
        ellipse(dst, 360 + i * 28, 520 + 6 * math.sin(t + i), 22, 5, rgb("#e8f0ff"), 0.12)
    return dst


def paint_coral_bloom(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#083246"), rgb("#0b1c28"), 0.6)
    glow(dst, 320, 80, 200, rgb("#3aa7b8"), 0.18)
    for i, (cx, cy, color) in enumerate(
        ((180, 470, "#e07a5f"), (260, 510, "#f2a65a"), (400, 490, "#d66853"), (480, 450, "#f4b183"))
    ):
        open_amt = 18 + 10 * (0.5 + 0.5 * math.sin(t + i))
        glow(dst, cx, cy, 70, rgb(color), 0.22)
        for k in range(7):
            ang = k * (math.pi / 6) - math.pi / 2 + 0.15 * math.sin(t)
            ellipse(dst, cx + math.cos(ang) * open_amt, cy + math.sin(ang) * open_amt * 0.7, 16, 28, rgb(color), 0.8)
        disc(dst, cx, cy + 8, 14, rgb("#f6d7b0"), 0.85)
    fish_x = 200 + 180 * math.sin(t)
    fish_y = 240 + 30 * math.cos(t * 2)
    ellipse(dst, fish_x, fish_y, 22, 10, rgb("#f0c14a"), 0.95)
    ellipse(dst, fish_x - 18, fish_y, 8, 8, rgb("#f0c14a"), 0.8)
    # bubbles
    for i in range(8):
        bx = 140 + i * 50
        by = (520 - (frame * 8 + i * 37) % 420)
        disc(dst, bx, by, 4 + i % 3, rgb("#d7f3f6"), 0.28)
    return dst


def paint_neon_dusk(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#1a0a24"), rgb("#0a0612"), 0.9)
    glow(dst, 320, 180, 220, rgb("#ff4d8d"), 0.16 + 0.06 * math.sin(t))
    glow(dst, 480, 220, 160, rgb("#3ee0ff"), 0.14 + 0.06 * math.cos(t))
    heights = [220, 280, 190, 310, 240, 200, 270, 230]
    x = 40
    for i, h in enumerate(heights):
        rect(dst, x, 640 - h, x + 70, 620, rgb("#120c18"), 0.96)
        window_on = 0.25 + 0.75 * (0.5 + 0.5 * math.sin(t * 2 + i * 1.3))
        for wy in range(640 - h + 16, 600, 22):
            rect(dst, x + 12, wy, x + 28, wy + 10, rgb("#3ee0ff"), 0.15 + 0.45 * window_on)
            rect(dst, x + 40, wy, x + 56, wy + 10, rgb("#ff4d8d"), 0.12 + 0.4 * (1 - window_on * 0.5))
        x += 76
    rect(dst, 0, 610, 640, 640, rgb("#08060c"), 1.0)
    rect(dst, 210, 300, 250, 318, rgb("#ff4d8d"), 0.55 + 0.4 * (0.5 + 0.5 * math.sin(t * 4)))
    rect(dst, 400, 340, 470, 356, rgb("#3ee0ff"), 0.5 + 0.4 * (0.5 + 0.5 * math.cos(t * 3)))
    return dst


def paint_firefly_grove(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#06140f"), rgb("#0a1c14"))
    for i, x0 in enumerate((40, 160, 300, 430, 540)):
        trunk_x = x0 + 20
        rect(dst, trunk_x, 280, trunk_x + 22, 600, rgb("#1a2a1c"), 0.95)
        glow(dst, trunk_x + 10, 240, 80, rgb("#14301c"), 0.5)
        ellipse(dst, trunk_x + 8, 220, 70 + 8 * math.sin(t + i), 90, rgb("#102418"), 0.7)
    glow(dst, 320, 520, 220, rgb("#0d2618"), 0.35)
    rng = np.random.default_rng(77)
    for i in range(28):
        seed = rng.random(3)
        x = 60 + seed[0] * 520 + 18 * math.sin(t + i * 0.7)
        y = 80 + seed[1] * 460 + 12 * math.cos(t * 1.2 + i)
        pulse = 0.25 + 0.75 * (0.5 + 0.5 * math.sin(t * 2 + i * 0.8))
        glow(dst, x, y, 10 + 6 * pulse, rgb("#f4e07a"), 0.55 * pulse)
        disc(dst, x, y, 2.4, rgb("#fff6b0"), 0.9 * pulse)
    return dst


def paint_corona(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#07060a"), rgb("#120c14"))
    xx, yy = grid()
    ang = np.arctan2(yy - 320, xx - 320)
    dist = np.sqrt((xx - 320) ** 2 + (yy - 320) ** 2)
    rays = 0.5 + 0.5 * np.cos(ang * 14 + t)
    flare = np.exp(-0.5 * ((dist - 110) / 70) ** 2) * (0.35 + 0.25 * rays)
    layer = blank()
    layer[..., :3] = mix(rgb("#f6d27a"), rgb("#c084fc"), 0.5 + 0.5 * np.sin(ang * 3 + t))
    layer[..., 3] = flare
    over(dst, layer)
    glow(dst, 320, 320, 160, rgb("#ffe9a8"), 0.28 + 0.08 * math.sin(t))
    disc(dst, 320, 320, 92, rgb("#050406"), 1.0, soft=2)
    disc(dst, 320, 320, 88, rgb("#0a0810"), 0.9)
    return dst


def paint_koi_mirror(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#12382c"), rgb("#0c241c"))
    glow(dst, 320, 200, 220, rgb("#3d8b6e"), 0.2)
    ellipse(dst, 320, 340, 260, 180, rgb("#0e2f26"), 0.9)
    ellipse(dst, 320, 340, 240, 160, rgb("#164a3a"), 0.55)
    for i, (amp, color, scale) in enumerate(((1.0, "#e76f3c", 1.0), (-1.0, "#f4efe6", 0.82), (0.4, "#d3542c", 0.7))):
        x = 320 + amp * 110 * math.cos(t + i)
        y = 340 + 70 * math.sin(t + i * 1.3)
        ellipse(dst, x, y, 28 * scale, 12 * scale, rgb(color), 0.92)
        ellipse(dst, x - 16 * amp, y, 10 * scale, 8 * scale, rgb(color), 0.7)
        disc(dst, x + 10 * amp, y - 2, 3, rgb("#1a1a1a"), 0.8)
    for i in range(6):
        lily_x = 180 + i * 70
        lily_y = 250 + 20 * math.sin(t + i)
        ellipse(dst, lily_x, lily_y, 22, 10, rgb("#2f6b45"), 0.7)
    glow(dst, 420, 220, 70, rgb("#d7ffe8"), 0.12 + 0.06 * math.sin(t))
    return dst


def paint_heat_shimmer(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#f2d3a2"), rgb("#c9844a"), 0.55)
    glow(dst, 480, 90, 160, rgb("#fff1c8"), 0.5)
    disc(dst, 500, 86, 38, rgb("#fff6d2"), 0.95)
    xx, yy = grid()
    dune = 420 + 28 * np.sin(xx / 70.0 + 0.4) + 10 * np.sin(xx / 28.0)
    sand = blank()
    sand[..., :3] = mix(rgb("#e0a56a"), rgb("#a65b2b"), (yy - 400) / 240)
    sand[..., 3] = smoothstep(dune - 8, dune + 10, yy)
    over(dst, sand)
    dune2 = 500 + 18 * np.sin(xx / 50.0 + 1.2)
    sand2 = blank()
    sand2[..., :3] = rgb("#8d4320")
    sand2[..., 3] = smoothstep(dune2 - 6, dune2 + 12, yy) * 0.85
    over(dst, sand2)
    wave = 0.08 + 0.06 * np.sin(xx / 16.0 + t * 2 + yy / 40.0)
    haze = blank()
    haze[..., :3] = rgb("#fff4d8")
    haze[..., 3] = ((yy > 240) & (yy < 430)).astype(np.float32) * wave
    over(dst, haze)
    return dst


def paint_ice_fracture(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#0b1730"), rgb("#16324f"))
    glow(dst, 320, 180, 200, rgb("#9ad4ff"), 0.16)
    ellipse(dst, 320, 400, 280, 150, rgb("#9ec9e6"), 0.55)
    ellipse(dst, 320, 400, 250, 130, rgb("#d7eef8"), 0.35)
    progress = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t))
    xx, yy = grid()
    crack_x = 200 + (yy - 280) * 0.35
    dist = np.abs(xx - crack_x)
    near = (yy > 260) & (yy < 280 + 240 * progress)
    layer = blank()
    layer[..., :3] = rgb("#f4fbff")
    layer[..., 3] = near.astype(np.float32) * smoothstep(10, 1.2, dist) * 0.9
    over(dst, layer)
    glow(dst, 320, 360, 80, rgb("#b9e7ff"), 0.18 * progress)
    for i in range(5):
        bx = 180 + i * 70
        by = 300 + 40 * i
        if by < 280 + 240 * progress:
            glow(dst, bx, by, 18, rgb("#e8f6ff"), 0.35)
    return dst


def paint_nave_light(frame: int) -> np.ndarray:
    t = phase(frame)
    dst = vertical_wash(rgb("#2a241c"), rgb("#16130f"))
    rect(dst, 40, 0, 160, 640, rgb("#3a3328"), 0.7)
    rect(dst, 480, 0, 600, 640, rgb("#3a3328"), 0.7)
    for i, x in enumerate((80, 200, 440, 560)):
        rect(dst, x - 16, 80, x + 16, 620, rgb("#4a4032"), 0.85)
        arch_y = 120
        glow(dst, x, arch_y, 40, rgb("#2a241c"), 0.4)
    shaft_x = 320 + 10 * math.sin(t)
    xx, yy = grid()
    left = shaft_x - 36 - yy * 0.02
    right = shaft_x + 36 + yy * 0.02
    shaft = ((xx > left) & (xx < right) & (yy > 40)).astype(np.float32)
    layer = blank()
    layer[..., :3] = rgb("#f0c878")
    layer[..., 3] = shaft * (0.12 + 0.08 * (1.0 - yy / H))
    over(dst, layer)
    glow(dst, shaft_x, 180, 90, rgb("#f6d48a"), 0.2 + 0.06 * math.sin(t))
    rng = np.random.default_rng(12)
    for i in range(30):
        seed = rng.random(3)
        x = shaft_x - 40 + seed[0] * 80 + 6 * math.sin(t + i)
        y = (40 + seed[1] * 560 + frame * 4 + i * 11) % 600
        disc(dst, x, y, 1.6, rgb("#fff3c8"), 0.35 + 0.35 * seed[2])
    rect(dst, 80, 560, 560, 640, rgb("#1c1812"), 0.9)
    glow(dst, shaft_x, 560, 70, rgb("#f0c878"), 0.16)
    return dst


PAINTERS = {
    1: paint_moonrise,
    2: paint_stained_glass,
    3: paint_petal_storm,
    4: paint_lighthouse,
    5: paint_coral_bloom,
    6: paint_neon_dusk,
    7: paint_firefly_grove,
    8: paint_corona,
    9: paint_koi_mirror,
    10: paint_heat_shimmer,
    11: paint_ice_fracture,
    12: paint_nave_light,
}


def render_work(work_id: int) -> list[Image.Image]:
    painter = PAINTERS[work_id]
    return [to_image(painter(frame)) for frame in range(FRAMES)]


def token_meta(work: dict) -> dict:
    attributes = [{"trait_type": key, "value": value} for key, value in work["attributes"].items()]
    return {
        "name": work["title"],
        "description": work["description"],
        "image": f"{work['id']}.gif",
        "external_url": f"/afterimages/{work['id']}",
        "attributes": attributes,
        "animation_loop": True,
        "compiler": "Afterimages 1:1 APNG",
    }


CSV_FIELDS = [
    "tokenID",
    "name",
    "description",
    "file_name",
    "attributes[Series]",
    "attributes[Palette]",
    "attributes[Motion]",
    "attributes[Season]",
    "attributes[Medium]",
]


def drop_csv_row(work: dict, meta: dict) -> dict:
    row = {
        "tokenID": work["id"],
        "name": meta["name"],
        "description": meta["description"],
        "file_name": f"{work['id']}.gif",
    }
    for attr in meta["attributes"]:
        row[f"attributes[{attr['trait_type']}]"] = attr["value"]
    return row


def build_brand(frames_by_id: dict[int, list[Image.Image]]) -> None:
    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    first = frames_by_id[1][0].copy()
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse((28, 28, SIZE - 28, SIZE - 28), fill=255)
    logo = first.copy()
    logo.putalpha(Image.composite(logo.split()[-1], Image.new("L", (SIZE, SIZE), 0), mask))
    logo.resize((512, 512), Image.Resampling.LANCZOS).save(BRAND_DIR / "logo-afterimages.png")
    save_apng([frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in frames_by_id[1]], BRAND_DIR / "logo-afterimages-loop.png")

    banner = Image.new("RGBA", (1500, 560), (18, 12, 10, 255))
    picks = (1, 8, 6)
    for i, work_id in enumerate(picks):
        face = frames_by_id[work_id][0].resize((420, 420), Image.Resampling.LANCZOS)
        banner.alpha_composite(face, (40 + i * 480, 90))
    draw = ImageDraw.Draw(banner)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 64)
        small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
    except OSError:
        font = ImageFont.load_default()
        small = font
    draw.text((56, 28), "AFTERIMAGES", font=font, fill=(255, 236, 210, 255))
    draw.text((60, 100), "One-of-one APNG paintings that never freeze.", font=small, fill=(232, 198, 160, 255))
    banner.convert("RGB").save(BRAND_DIR / "banner-afterimages.png", quality=94)

    gif_source = frames_by_id[8]
    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS).convert("RGB") for frame in gif_source]
    palette = gif_frames[0].quantize(colors=240, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    gif_q = [frame.quantize(palette=palette, dither=Image.Dither.FLOYDSTEINBERG) for frame in gif_frames]
    gif_q[0].save(
        BRAND_DIR / "collection-afterimages.gif",
        save_all=True,
        append_images=gif_q[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )


def write_sidecars(rows: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "opensea-metadata.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    (OUT / "README.md").write_text(
        "# Afterimages OpenSea pack\n\n"
        "12 unique 1:1 loops at 640×640, 16 frames, 100ms.\n\n"
        "Upload every file in `gifs/` (1.gif–12.gif) plus `opensea-metadata.csv` to an OpenSea Drop.\n"
        "OpenSea Drops play GIF, not APNG. Site previews stay APNG in public/afterimages/.\n"
        "The CSV uses OpenSea Studio headers: `tokenID`, `name`, `description`, `file_name`, and `attributes[Trait]`.\n",
        encoding="utf-8",
    )
    (META_DIR).mkdir(parents=True, exist_ok=True)
    (META_DIR / "afterimages.json").write_text(
        json.dumps(
            {
                "name": "Afterimages",
                "symbol": "AFTER",
                "description": "Afterimages is a 12-piece OpenSea drop of unique looping paintings. Each token is a finished APNG — not stacked traits, not a generative shuffle. One canvas, one clock, one artwork. Minting on Robinhood Chain.",
                "image": "/brand/collection-afterimages.gif",
                "banner_image": "/brand/banner-afterimages.png",
                "external_link": "/afterimages",
                "seller_fee_basis_points": 750,
                "fee_recipient": "0x0000000000000000000000000000000000000000",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    GIF_DIR.mkdir(parents=True, exist_ok=True)
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    frames_by_id: dict[int, list[Image.Image]] = {}
    rows: list[dict] = []
    print("Painting Afterimages 1:1 APNGs…")
    for work in WORKS:
        print(f"  #{work['id']} {work['title']}")
        frames = render_work(work["id"])
        frames_by_id[work["id"]] = frames
        site_path = PUBLIC_DIR / f"{work['id']}.png"
        drop_path = IMAGE_DIR / f"{work['id']}.png"
        save_apng(frames, site_path)
        drop_path.write_bytes(site_path.read_bytes())
        save_loop_gif(frames, GIF_DIR / f"{work['id']}.gif", DURATION_MS)
        meta = token_meta(work)
        (JSON_DIR / f"{work['id']}.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        rows.append(drop_csv_row(work, meta))
    print("Writing brand and OpenSea sidecars…")
    build_brand(frames_by_id)
    write_sidecars(rows)
    print("Done.")


if __name__ == "__main__":
    main()
