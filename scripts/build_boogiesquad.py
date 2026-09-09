#!/usr/bin/env python3
"""Paint Boogie Squad — jelly-cel party dancers on a 12-frame groove.

Soft vinyl fills, cream outlines, sausage limbs, a side-step that reads as dance.
Not doodle ink. Not sticker cutouts. Not oval-egg bodies. Not charcoal LINE=11.

Stack: stage → lights → cast → face → fit → prop
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

from paint_kit import DURATION_MS, FRAMES, SIZE, place_portrait, save_apng, save_image  # noqa: E402
from gif_bake import save_loop_gif  # noqa: E402

NAME = "Boogie Squad"
SYMBOL = "BOOG"
TOKEN = "Boogie"
SLUG = "boogiesquad"
TRAIT_DIR = ROOT / "public" / f"{SLUG}-traits"
PREVIEW_DIR = ROOT / "public" / f"{SLUG}-preview"
BRAND_DIR = ROOT / "public" / "brand"
META_DIR = ROOT / "public" / "metadata"
SRC_DATA = ROOT / "src" / "data"

INK = (22, 14, 48, 255)
CREAM = (255, 244, 232, 255)
BLUSH = (255, 132, 168, 255)
LINE = 8
CX = 256.0

STAGES = ("floor", "disco", "rooftop", "alley", "booth", "backyard", "warehouse")
LIGHTS = ("none", "spots", "glitter", "neon", "confetti", "rings")
CASTS = (
    "cat-peach",
    "cat-midnight",
    "frog-lime",
    "frog-teal",
    "blob-grape",
    "blob-mango",
    "bird-canary",
    "bird-indigo",
    "robot-chrome",
    "robot-candy",
    "bunny-cream",
    "pig-blush",
)
FACES = ("hype", "cool", "wink", "blep", "focus", "scream", "grin", "heart")
FITS = ("none", "hoodie", "shades", "jacket", "phones", "chain", "visor")
PROPS = ("none", "mic", "boombox", "sticks", "vinyl", "drink", "trophy")

CAST_PAL = {
    "cat-peach": {"fill": (255, 168, 132), "shade": (232, 118, 96), "accent": (255, 214, 186), "kind": "cat"},
    "cat-midnight": {"fill": (72, 64, 128), "shade": (44, 36, 88), "accent": (168, 156, 214), "kind": "cat"},
    "frog-lime": {"fill": (118, 214, 86), "shade": (62, 156, 58), "accent": (196, 244, 140), "kind": "frog"},
    "frog-teal": {"fill": (48, 176, 164), "shade": (28, 118, 124), "accent": (140, 228, 210), "kind": "frog"},
    "blob-grape": {"fill": (168, 92, 214), "shade": (112, 48, 168), "accent": (214, 168, 244), "kind": "blob"},
    "blob-mango": {"fill": (255, 176, 64), "shade": (232, 124, 32), "accent": (255, 220, 140), "kind": "blob"},
    "bird-canary": {"fill": (255, 214, 64), "shade": (232, 164, 28), "accent": (255, 244, 168), "kind": "bird"},
    "bird-indigo": {"fill": (86, 92, 196), "shade": (48, 52, 148), "accent": (168, 176, 244), "kind": "bird"},
    "robot-chrome": {"fill": (188, 198, 214), "shade": (118, 128, 148), "accent": (236, 244, 255), "kind": "robot"},
    "robot-candy": {"fill": (255, 96, 148), "shade": (196, 48, 110), "accent": (255, 186, 210), "kind": "robot"},
    "bunny-cream": {"fill": (255, 228, 214), "shade": (232, 176, 168), "accent": (255, 246, 236), "kind": "bunny"},
    "pig-blush": {"fill": (255, 164, 176), "shade": (220, 108, 128), "accent": (255, 210, 214), "kind": "pig"},
}


def rgba(rgb: tuple[int, int, int], a: int = 255) -> tuple[int, int, int, int]:
    return (rgb[0], rgb[1], rgb[2], a)


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def groove(frame: int) -> dict[str, float]:
    t = frame / FRAMES * math.tau
    s = math.sin(t)
    c = math.cos(t)
    dx = s * 16.0
    dy = -abs(s) * 11.0
    lean = s * 7.0
    return {
        "t": t,
        "s": s,
        "c": c,
        "dx": dx,
        "dy": dy,
        "lean": lean,
        "hx": CX + dx + lean * 0.35,
        "hy": 196.0 + dy,
        "tx": CX + dx,
        "ty": 314.0 + dy,
        "lx": CX + dx - 24.0 - s * 16.0,
        "rx": CX + dx + 24.0 + s * 16.0,
        "fy": 430.0 + dy * 0.25,
        "alx": CX + dx - 62.0 + c * 10.0,
        "aly": 298.0 + dy - s * 24.0,
        "arx": CX + dx + 66.0 + s * 12.0,
        "ary": 304.0 + dy + c * 22.0,
    }


def disk(draw: ImageDraw.ImageDraw, x: float, y: float, r: float, fill, width: int = LINE) -> None:
    draw.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=INK, width=width)


def oval(draw: ImageDraw.ImageDraw, x: float, y: float, rx: float, ry: float, fill, width: int = LINE) -> None:
    draw.ellipse((x - rx, y - ry, x + rx, y + ry), fill=fill, outline=INK, width=width)


def capsule(draw: ImageDraw.ImageDraw, x1: float, y1: float, x2: float, y2: float, r: float, fill) -> None:
    ink_w = int(r * 2) + LINE
    fill_w = int(r * 2)
    draw.line([(x1, y1), (x2, y2)], fill=INK, width=ink_w)
    draw.line([(x1, y1), (x2, y2)], fill=fill, width=fill_w)
    ir = r + LINE / 2
    draw.ellipse((x1 - ir, y1 - ir, x1 + ir, y1 + ir), fill=INK)
    draw.ellipse((x2 - ir, y2 - ir, x2 + ir, y2 + ir), fill=INK)
    draw.ellipse((x1 - r, y1 - r, x1 + r, y1 + r), fill=fill)
    draw.ellipse((x2 - r, y2 - r, x2 + r, y2 + r), fill=fill)


def wash(top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    y = np.linspace(0.0, 1.0, SIZE, dtype=np.float32)[:, None]
    row = np.array(top, dtype=np.float32) * (1.0 - y) + np.array(bottom, dtype=np.float32) * y
    rgb = np.repeat(row[:, None, :], SIZE, axis=1)
    alpha = np.full((SIZE, SIZE, 1), 255, dtype=np.uint8)
    arr = np.concatenate([np.clip(rgb, 0, 255).astype(np.uint8), alpha], axis=2)
    return Image.fromarray(arr, "RGBA")


def paint_stage(kind: str, frame: int) -> Image.Image:
    pulse = 0.5 + 0.5 * math.sin(frame / FRAMES * math.tau)
    if kind == "floor":
        img = wash((28, 12, 64), (12, 8, 28))
        draw = ImageDraw.Draw(img)
        for row in range(7):
            for col in range(8):
                x0, y0 = 16 + col * 62, 268 + row * 36
                color = (255, 64, 168) if (row + col) % 2 == 0 else (64, 220, 255)
                a = 90 + int(40 * pulse)
                draw.polygon([(x0, y0 + 18), (x0 + 36, y0), (x0 + 72, y0 + 18), (x0 + 36, y0 + 36)], fill=(*color, a))
        draw.ellipse((40, 40, 472, 220), fill=(255, 80, 180, 40))
        return img
    if kind == "disco":
        img = wash((16, 8, 36), (8, 4, 18))
        draw = ImageDraw.Draw(img)
        draw.ellipse((176, -40, 336, 120), fill=(220, 230, 255, 220), outline=INK, width=6)
        for i in range(14):
            ang = i / 14 * math.tau + frame / FRAMES * math.tau
            x = 256 + math.cos(ang) * 70
            y = 40 + math.sin(ang) * 28
            draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(255, 240, 120, 200))
        draw.polygon([(40, 512), (120, 300), (200, 512)], fill=(255, 40, 160, 50))
        draw.polygon([(312, 512), (392, 280), (472, 512)], fill=(40, 220, 255, 50))
        return img
    if kind == "rooftop":
        img = wash((28, 24, 72), (255, 96, 64))
        draw = ImageDraw.Draw(img)
        draw.polygon([(0, 250), (80, 170), (140, 250)], fill=(18, 14, 40, 255))
        draw.polygon([(160, 260), (220, 150), (300, 260)], fill=(22, 16, 48, 255))
        draw.polygon([(340, 240), (420, 130), (512, 240)], fill=(16, 12, 36, 255))
        draw.rectangle((0, 360, 512, 512), fill=(48, 36, 56, 255), outline=INK, width=6)
        for i in range(6):
            draw.ellipse((40 + i * 80, 120 + (i % 3) * 18, 52 + i * 80, 132 + (i % 3) * 18), fill=(255, 220, 80, 220))
        return img
    if kind == "alley":
        img = wash((18, 10, 28), (48, 8, 64))
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, 90, 512), fill=(28, 16, 40, 255))
        draw.rectangle((422, 0, 512, 512), fill=(28, 16, 40, 255))
        draw.rectangle((16, 80, 74, 220), fill=(255, 40, 160, 180), outline=INK, width=5)
        draw.rectangle((438, 140, 496, 280), fill=(40, 255, 200, 180), outline=INK, width=5)
        draw.rectangle((0, 390, 512, 512), fill=(22, 14, 30, 255))
        return img
    if kind == "booth":
        img = wash((48, 16, 36), (18, 8, 22))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((20, 240, 492, 520), radius=48, fill=(92, 24, 48, 255), outline=INK, width=8)
        draw.rounded_rectangle((70, 200, 442, 300), radius=30, fill=(140, 40, 72, 255), outline=INK, width=7)
        draw.ellipse((60, 40, 200, 160), fill=(255, 80, 140, 50))
        return img
    if kind == "backyard":
        img = wash((36, 48, 92), (18, 72, 64))
        draw = ImageDraw.Draw(img)
        draw.ellipse((-40, 360, 200, 560), fill=(28, 92, 48, 255))
        draw.ellipse((320, 380, 560, 580), fill=(22, 80, 44, 255))
        for i in range(8):
            x = 36 + i * 60
            sway = math.sin(frame / FRAMES * math.tau + i) * 4
            draw.line([(x, 40), (x + sway, 160)], fill=(255, 214, 80, 220), width=3)
            draw.ellipse((x + sway - 8, 150, x + sway + 8, 166), fill=(255, 180, 40, 230))
        draw.rectangle((0, 420, 512, 512), fill=(64, 44, 28, 255))
        return img
    img = wash((24, 22, 36), (12, 10, 18))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 512, 80), fill=(40, 36, 52, 255))
    for i in range(5):
        x = 50 + i * 90
        glow = 80 + int(80 * pulse) if i % 2 == frame % 2 else 40
        draw.ellipse((x, 20, x + 36, 56), fill=(255, 220, 80, glow))
    draw.rectangle((0, 400, 512, 512), fill=(28, 24, 36, 255))
    return img


def paint_lights(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    img = blank()
    draw = ImageDraw.Draw(img)
    t = frame / FRAMES * math.tau
    if kind == "spots":
        for i, color in enumerate(((255, 80, 180), (80, 220, 255), (255, 220, 60))):
            ang = t + i * 2.1
            x = 256 + math.cos(ang) * 70
            draw.polygon([(x - 50, 0), (x + 50, 0), (x + 90, 512), (x - 90, 512)], fill=(*color, 28))
        return img
    if kind == "glitter":
        rng = np.random.default_rng(17 + frame)
        for _ in range(28):
            x, y = int(rng.integers(30, 480)), int(rng.integers(20, 200))
            r = int(rng.integers(3, 8))
            draw.ellipse((x, y, x + r, y + r), fill=(255, 250, 200, 200))
        return img
    if kind == "neon":
        glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow)
        gdraw.ellipse((40, 40, 472, 472), outline=(255, 40, 180, 90), width=18)
        gdraw.ellipse((70, 70, 442, 442), outline=(40, 255, 220, 70), width=12)
        return glow.filter(ImageFilter.GaussianBlur(3))
    if kind == "confetti":
        rng = np.random.default_rng(9)
        colors = ((255, 80, 180), (80, 255, 200), (255, 220, 60), (120, 160, 255))
        for i in range(36):
            fall = (frame * 14 + i * 37) % 520
            x = 20 + (i * 47) % 470
            y = (fall + i * 11) % 520 - 20
            w, h = 10, 6
            draw.rectangle((x, y, x + w, y + h), fill=(*colors[i % 4], 220))
        return img
    for i in range(3):
        r = 70 + i * 46 + math.sin(t + i) * 8
        a = 70 - i * 16
        draw.ellipse((256 - r, 300 - r * 0.35, 256 + r, 300 + r * 0.35), outline=(255, 240, 120, a), width=5)
    return img


def _shade(rgb: tuple[int, int, int]) -> tuple[int, int, int, int]:
    return rgba(rgb)


def paint_cast(kind: str, frame: int) -> Image.Image:
    pal = CAST_PAL[kind]
    fill, shade, accent, species = pal["fill"], pal["shade"], pal["accent"], pal["kind"]
    g = groove(frame)
    img = blank()
    draw = ImageDraw.Draw(img)
    hx, hy, tx, ty = g["hx"], g["hy"], g["tx"], g["ty"]
    fill_c, shade_c, accent_c = rgba(fill), rgba(shade), rgba(accent)

    if species != "blob":
        capsule(draw, tx - 8, ty + 10, g["lx"], g["fy"], 16, fill_c)
        capsule(draw, tx + 8, ty + 10, g["rx"], g["fy"], 16, fill_c)
        oval(draw, g["lx"], g["fy"] + 8, 20, 10, (36, 28, 48, 255), width=6)
        oval(draw, g["rx"], g["fy"] + 8, 20, 10, (36, 28, 48, 255), width=6)
        oval(draw, g["lx"], g["fy"] + 4, 18, 8, (255, 80, 180, 255), width=5)
        oval(draw, g["rx"], g["fy"] + 4, 18, 8, (80, 220, 255, 255), width=5)

    capsule(draw, tx - 18, ty - 10, g["alx"], g["aly"], 14, fill_c)
    capsule(draw, tx + 18, ty - 10, g["arx"], g["ary"], 14, fill_c)

    if species == "blob":
        oval(draw, tx, ty + 36, 92, 78, fill_c)
        oval(draw, tx - 18, ty + 16, 36, 22, accent_c, width=6)
        oval(draw, tx, g["fy"] + 6, 70, 18, shade_c, width=6)
    elif species == "robot":
        draw.rounded_rectangle((tx - 52, ty - 30, tx + 52, ty + 70), radius=16, fill=fill_c, outline=INK, width=LINE)
        oval(draw, tx, ty - 8, 28, 12, accent_c, width=6)
        draw.rectangle((tx - 22, ty + 16, tx + 22, ty + 44), fill=shade_c, outline=INK, width=5)
    else:
        oval(draw, tx, ty + 16, 62, 58, fill_c)
        oval(draw, tx - 14, ty - 4, 22, 14, accent_c, width=6)

    if species == "cat":
        disk(draw, hx, hy, 72, fill_c)
        draw.polygon([(hx - 54, hy - 18), (hx - 38, hy - 86), (hx - 10, hy - 40)], fill=fill_c, outline=INK)
        draw.polygon([(hx + 54, hy - 18), (hx + 38, hy - 86), (hx + 10, hy - 40)], fill=fill_c, outline=INK)
        draw.polygon([(hx - 48, hy - 20), (hx - 38, hy - 68), (hx - 18, hy - 36)], fill=shade_c)
        oval(draw, tx + 58, ty + 40, 18, 28, fill_c, width=6)
    elif species == "frog":
        oval(draw, hx, hy + 8, 80, 62, fill_c)
        disk(draw, hx - 38, hy - 36, 26, fill_c)
        disk(draw, hx + 38, hy - 36, 26, fill_c)
        oval(draw, hx, hy + 28, 36, 14, accent_c, width=5)
    elif species == "blob":
        disk(draw, hx, hy + 10, 86, fill_c)
        oval(draw, hx - 20, hy - 10, 28, 16, accent_c, width=6)
    elif species == "bird":
        disk(draw, hx, hy, 68, fill_c)
        draw.polygon([(hx + 50, hy + 8), (hx + 98, hy + 18), (hx + 50, hy + 32)], fill=(255, 140, 48, 255), outline=INK)
        oval(draw, tx + 50, ty + 8, 28, 18, fill_c, width=6)
    elif species == "robot":
        draw.rounded_rectangle((hx - 62, hy - 58, hx + 62, hy + 58), radius=18, fill=fill_c, outline=INK, width=LINE)
        draw.line([(hx, hy - 58), (hx, hy - 88)], fill=INK, width=7)
        disk(draw, hx, hy - 94, 10, (255, 80, 180, 255), width=5)
        draw.rounded_rectangle((hx - 40, hy - 18, hx + 40, hy + 16), radius=10, fill=(40, 220, 255, 255), outline=INK, width=5)
    elif species == "bunny":
        disk(draw, hx, hy, 70, fill_c)
        oval(draw, hx - 32, hy - 88, 16, 42, fill_c)
        oval(draw, hx + 32, hy - 88, 16, 42, fill_c)
        oval(draw, hx - 32, hy - 84, 8, 28, (255, 164, 176, 255), width=5)
        oval(draw, hx + 32, hy - 84, 8, 28, (255, 164, 176, 255), width=5)
    else:
        disk(draw, hx, hy, 72, fill_c)
        oval(draw, hx - 48, hy - 28, 18, 22, fill_c, width=6)
        oval(draw, hx + 48, hy - 28, 18, 22, fill_c, width=6)
        oval(draw, hx, hy + 18, 22, 16, (255, 186, 190, 255), width=6)
        disk(draw, hx - 8, hy + 16, 4, INK, width=2)
        disk(draw, hx + 8, hy + 16, 4, INK, width=2)

    oval(draw, hx - 22, hy + 22, 14, 8, BLUSH, width=0)
    oval(draw, hx + 22, hy + 22, 14, 8, BLUSH, width=0)
    return img


def paint_face(kind: str, frame: int) -> Image.Image:
    g = groove(frame)
    hx, hy = g["hx"], g["hy"]
    img = blank()
    draw = ImageDraw.Draw(img)
    blink = frame % FRAMES in (3, 4)

    def eye(x: float, y: float, open_eye: bool = True, heart: bool = False) -> None:
        if heart:
            draw.polygon([(x, y + 10), (x - 14, y - 4), (x, y - 2), (x + 14, y - 4)], fill=(255, 72, 120, 255), outline=INK)
            return
        if open_eye:
            disk(draw, x, y, 13, CREAM, width=6)
            disk(draw, x + 3, y + 1, 6, INK, width=2)
            disk(draw, x + 5, y - 2, 2, CREAM, width=0)
        else:
            draw.arc((x - 12, y - 6, x + 12, y + 8), 20, 160, fill=INK, width=6)

    if kind == "hype":
        eye(hx - 22, hy - 6, not blink)
        eye(hx + 22, hy - 6, not blink)
        oval(draw, hx, hy + 28, 18, 16, (40, 20, 40, 255), width=6)
        draw.arc((hx - 16, hy + 18, hx + 16, hy + 38), 200, 340, fill=CREAM, width=4)
    elif kind == "cool":
        eye(hx - 22, hy - 2, not blink)
        eye(hx + 22, hy - 2, not blink)
        draw.arc((hx - 22, hy + 18, hx + 22, hy + 40), 20, 160, fill=INK, width=6)
    elif kind == "wink":
        eye(hx - 22, hy - 6, False)
        eye(hx + 22, hy - 6, not blink)
        draw.arc((hx - 16, hy + 20, hx + 16, hy + 42), 10, 170, fill=INK, width=6)
    elif kind == "blep":
        eye(hx - 22, hy - 6, not blink)
        eye(hx + 22, hy - 6, not blink)
        oval(draw, hx, hy + 26, 12, 8, (40, 20, 40, 255), width=5)
        draw.polygon([(hx + 4, hy + 28), (hx + 22, hy + 44), (hx + 2, hy + 36)], fill=(255, 96, 140, 255), outline=INK)
    elif kind == "focus":
        eye(hx - 22, hy - 4, not blink)
        eye(hx + 22, hy - 4, not blink)
        draw.line([(hx - 10, hy + 26), (hx + 10, hy + 26)], fill=INK, width=6)
        draw.arc((hx - 28, hy - 28, hx - 8, hy - 10), 200, 340, fill=INK, width=5)
        draw.arc((hx + 8, hy - 28, hx + 28, hy - 10), 200, 340, fill=INK, width=5)
    elif kind == "scream":
        eye(hx - 24, hy - 10, True)
        eye(hx + 24, hy - 10, True)
        oval(draw, hx, hy + 30, 16, 20, (40, 20, 40, 255), width=6)
    elif kind == "grin":
        eye(hx - 22, hy - 6, not blink)
        eye(hx + 22, hy - 6, not blink)
        draw.arc((hx - 24, hy + 14, hx + 24, hy + 48), 10, 170, fill=INK, width=7)
        draw.line([(hx - 10, hy + 30), (hx - 10, hy + 40)], fill=INK, width=4)
        draw.line([(hx + 10, hy + 30), (hx + 10, hy + 40)], fill=INK, width=4)
    else:
        eye(hx - 22, hy - 6, True, heart=True)
        eye(hx + 22, hy - 6, True, heart=True)
        oval(draw, hx, hy + 28, 10, 8, (255, 96, 140, 255), width=5)
    return img


def paint_fit(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    g = groove(frame)
    hx, hy, tx, ty = g["hx"], g["hy"], g["tx"], g["ty"]
    img = blank()
    draw = ImageDraw.Draw(img)
    if kind == "hoodie":
        draw.polygon(
            [(tx - 70, ty + 50), (tx - 58, ty - 36), (hx - 40, hy + 40), (hx + 40, hy + 40), (tx + 58, ty - 36), (tx + 70, ty + 50)],
            fill=(72, 48, 196, 255),
            outline=INK,
        )
        oval(draw, hx, hy + 48, 36, 16, (48, 32, 140, 255), width=6)
        draw.polygon([(hx - 20, hy + 40), (hx - 8, hy + 70), (hx - 28, hy + 66)], fill=(255, 80, 180, 255), outline=INK)
    elif kind == "shades":
        draw.rounded_rectangle((hx - 48, hy - 16, hx - 4, hy + 10), radius=8, fill=(18, 12, 32, 255), outline=INK, width=5)
        draw.rounded_rectangle((hx + 4, hy - 16, hx + 48, hy + 10), radius=8, fill=(18, 12, 32, 255), outline=INK, width=5)
        draw.line([(hx - 4, hy - 4), (hx + 4, hy - 4)], fill=INK, width=5)
        draw.line([(hx - 48, hy - 6), (hx - 62, hy - 10)], fill=INK, width=5)
        draw.line([(hx + 48, hy - 6), (hx + 62, hy - 10)], fill=INK, width=5)
    elif kind == "jacket":
        draw.polygon(
            [(tx - 72, ty + 56), (tx - 54, ty - 28), (tx + 54, ty - 28), (tx + 72, ty + 56)],
            fill=(255, 80, 160, 255),
            outline=INK,
        )
        draw.line([(tx, ty - 20), (tx, ty + 50)], fill=INK, width=6)
        oval(draw, tx - 18, ty + 8, 6, 6, (255, 220, 80, 255), width=3)
        oval(draw, tx + 18, ty + 8, 6, 6, (255, 220, 80, 255), width=3)
    elif kind == "phones":
        oval(draw, hx - 58, hy, 16, 22, (36, 28, 48, 255), width=6)
        oval(draw, hx + 58, hy, 16, 22, (36, 28, 48, 255), width=6)
        draw.arc((hx - 58, hy - 70, hx + 58, hy + 10), 200, 340, fill=INK, width=8)
        oval(draw, hx - 58, hy, 10, 14, (255, 80, 180, 255), width=4)
        oval(draw, hx + 58, hy, 10, 14, (80, 220, 255, 255), width=4)
    elif kind == "chain":
        for i, xoff in enumerate((-16, 0, 16)):
            disk(draw, tx + xoff, ty + 8 + abs(i - 1) * 6, 9, (255, 214, 64, 255), width=5)
        draw.arc((tx - 28, ty - 16, tx + 28, ty + 28), 10, 170, fill=(255, 214, 64, 255), width=6)
    else:
        draw.rounded_rectangle((hx - 50, hy - 28, hx + 50, hy + 6), radius=10, fill=(40, 255, 200, 255), outline=INK, width=6)
        draw.line([(hx - 8, hy - 28), (hx - 8, hy - 44)], fill=INK, width=5)
        disk(draw, hx - 8, hy - 48, 6, (255, 80, 180, 255), width=4)
    return img


def paint_prop(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    g = groove(frame)
    x, y = g["arx"] + 8, g["ary"] + 6
    img = blank()
    draw = ImageDraw.Draw(img)
    if kind == "mic":
        disk(draw, x, y - 16, 14, (220, 228, 240, 255), width=6)
        draw.line([(x, y - 4), (x, y + 28)], fill=INK, width=8)
        oval(draw, x, y + 30, 8, 5, (255, 80, 180, 255), width=4)
    elif kind == "boombox":
        draw.rounded_rectangle((x - 36, y - 18, x + 36, y + 22), radius=8, fill=(48, 36, 72, 255), outline=INK, width=6)
        disk(draw, x - 16, y + 2, 10, (80, 220, 255, 255), width=5)
        disk(draw, x + 16, y + 2, 10, (255, 80, 180, 255), width=5)
        draw.rectangle((x - 8, y - 12, x + 8, y - 4), fill=(255, 220, 80, 255), outline=INK, width=3)
    elif kind == "sticks":
        draw.line([(x - 10, y + 18), (x - 22, y - 28)], fill=(255, 80, 180, 255), width=8)
        draw.line([(x + 8, y + 18), (x + 26, y - 26)], fill=(80, 255, 200, 255), width=8)
        disk(draw, x - 22, y - 30, 7, (255, 240, 200, 255), width=4)
        disk(draw, x + 26, y - 28, 7, (255, 240, 200, 255), width=4)
    elif kind == "vinyl":
        disk(draw, x, y, 26, (28, 20, 40, 255), width=6)
        disk(draw, x, y, 8, (255, 80, 180, 255), width=4)
        disk(draw, x, y, 3, CREAM, width=0)
    elif kind == "drink":
        draw.polygon([(x - 12, y - 8), (x + 12, y - 8), (x + 8, y + 22), (x - 8, y + 22)], fill=(80, 255, 200, 200), outline=INK)
        draw.line([(x + 12, y - 8), (x + 22, y - 28)], fill=(255, 80, 180, 255), width=5)
        disk(draw, x + 22, y - 32, 6, (255, 240, 120, 255), width=3)
    else:
        draw.polygon([(x, y - 28), (x + 22, y - 8), (x + 14, y + 18), (x - 14, y + 18), (x - 22, y - 8)], fill=(255, 214, 64, 255), outline=INK)
        oval(draw, x, y + 22, 16, 6, (196, 148, 32, 255), width=5)
    return img


TRAIT_SPEC = {
    "stage": [
        ("floor", "Dance Floor", 22),
        ("disco", "Disco Hall", 16),
        ("rooftop", "Rooftop Party", 14),
        ("alley", "Neon Alley", 14),
        ("booth", "Club Booth", 12),
        ("backyard", "Backyard Jam", 12),
        ("warehouse", "Warehouse Rave", 10),
    ],
    "lights": [
        ("none", "None", 28),
        ("spots", "Spotlights", 18),
        ("glitter", "Disco Glints", 16),
        ("neon", "Neon Glow", 14),
        ("confetti", "Confetti Burst", 14),
        ("rings", "Beat Rings", 10),
    ],
    "cast": [
        ("cat-peach", "Peach Cat", 14),
        ("cat-midnight", "Midnight Cat", 10),
        ("frog-lime", "Lime Frog", 12),
        ("frog-teal", "Teal Frog", 9),
        ("blob-grape", "Grape Blob", 10),
        ("blob-mango", "Mango Blob", 8),
        ("bird-canary", "Canary Bird", 10),
        ("bird-indigo", "Indigo Bird", 7),
        ("robot-chrome", "Chrome Robot", 8),
        ("robot-candy", "Candy Robot", 5),
        ("bunny-cream", "Cream Bunny", 4),
        ("pig-blush", "Blush Pig", 3),
    ],
    "face": [
        ("hype", "Hype", 18),
        ("cool", "Cool", 16),
        ("wink", "Wink", 14),
        ("blep", "Tongue Out", 12),
        ("grin", "Grin", 12),
        ("focus", "Focused", 10),
        ("scream", "Party Scream", 10),
        ("heart", "Heart Eyes", 8),
    ],
    "fit": [
        ("none", "None", 26),
        ("hoodie", "Hoodie", 16),
        ("shades", "Shades", 14),
        ("jacket", "Jacket", 14),
        ("phones", "Headphones", 12),
        ("chain", "Chain", 10),
        ("visor", "Visor", 8),
    ],
    "prop": [
        ("none", "None", 28),
        ("mic", "Mic", 16),
        ("boombox", "Boombox", 14),
        ("sticks", "Glow Sticks", 14),
        ("vinyl", "Vinyl", 12),
        ("drink", "Drink", 10),
        ("trophy", "Trophy", 6),
    ],
}

PAINTERS = {
    "stage": {k: (lambda kind: (lambda frame, k=kind: paint_stage(k, frame)))(k) for k in STAGES},
    "lights": {k: (lambda kind: (lambda frame, k=kind: paint_lights(k, frame)))(k) for k in LIGHTS},
    "cast": {k: (lambda kind: (lambda frame, k=kind: paint_cast(k, frame)))(k) for k in CASTS},
    "face": {k: (lambda kind: (lambda frame, k=kind: paint_face(k, frame)))(k) for k in FACES},
    "fit": {k: (lambda kind: (lambda frame, k=kind: paint_fit(k, frame)))(k) for k in FITS},
    "prop": {k: (lambda kind: (lambda frame, k=kind: paint_prop(k, frame)))(k) for k in PROPS},
}

STACK = ("stage", "lights", "cast", "face", "fit", "prop")

SIGNATURES = [
    {"stage": "floor", "lights": "none", "cast": "cat-peach", "face": "hype", "fit": "none", "prop": "none"},
    {"stage": "disco", "lights": "glitter", "cast": "frog-lime", "face": "grin", "fit": "shades", "prop": "mic"},
    {"stage": "rooftop", "lights": "spots", "cast": "blob-grape", "face": "scream", "fit": "hoodie", "prop": "boombox"},
    {"stage": "alley", "lights": "neon", "cast": "bird-canary", "face": "wink", "fit": "phones", "prop": "vinyl"},
    {"stage": "booth", "lights": "rings", "cast": "robot-chrome", "face": "cool", "fit": "visor", "prop": "sticks"},
    {"stage": "backyard", "lights": "confetti", "cast": "bunny-cream", "face": "heart", "fit": "jacket", "prop": "drink"},
    {"stage": "warehouse", "lights": "spots", "cast": "pig-blush", "face": "blep", "fit": "chain", "prop": "trophy"},
    {"stage": "disco", "lights": "neon", "cast": "cat-midnight", "face": "focus", "fit": "hoodie", "prop": "mic"},
    {"stage": "floor", "lights": "glitter", "cast": "frog-teal", "face": "hype", "fit": "shades", "prop": "sticks"},
    {"stage": "rooftop", "lights": "none", "cast": "blob-mango", "face": "grin", "fit": "none", "prop": "vinyl"},
    {"stage": "alley", "lights": "confetti", "cast": "bird-indigo", "face": "wink", "fit": "jacket", "prop": "boombox"},
    {"stage": "booth", "lights": "spots", "cast": "robot-candy", "face": "scream", "fit": "phones", "prop": "none"},
    {"stage": "backyard", "lights": "rings", "cast": "cat-peach", "face": "cool", "fit": "visor", "prop": "drink"},
    {"stage": "warehouse", "lights": "neon", "cast": "frog-lime", "face": "heart", "fit": "chain", "prop": "mic"},
    {"stage": "disco", "lights": "confetti", "cast": "bunny-cream", "face": "blep", "fit": "hoodie", "prop": "trophy"},
    {"stage": "floor", "lights": "spots", "cast": "robot-chrome", "face": "hype", "fit": "shades", "prop": "boombox"},
]

TRAIT_LABELS = (
    ("stage", "Stage"),
    ("lights", "Lights"),
    ("cast", "Cast"),
    ("face", "Face"),
    ("fit", "Fit"),
    ("prop", "Prop"),
)

COLLECTION_DESCRIPTION = (
    "Boogie Squad is a 10,000-piece collection of looping jelly-cel dance PFP GIFs on Robinhood Chain. "
    "Each dancer is stacked from six layers — stage, lights, cast, face, fit, and prop — then flattened onto one 12-frame GIF. "
    "Cats, frogs, blobs, birds, robots, and more. A side-step. A groove. One shared clock."
)

COLLECTION_STORY = (
    "Boogie Squad.\n\n"
    "A 10,000-piece collection of looping jelly-cel dance PFP GIFs on Robinhood Chain. "
    "Each Boogie is stacked from six layers — stage, lights, cast, face, fit, and prop — then flattened onto one 12-frame GIF. "
    "Mixed cartoon dancers: cats, frogs, blobs, birds, little robots, bunnies, and pigs. "
    "Species is a trait. The floor is a trait. The groove is the loop.\n\n"
    "Soft vinyl fills. Cream outlines. Sausage limbs. Visible feet that step. "
    "Not a sticker fox. Not a bust-crop cat. Not a musical note. Not a risograph plate. "
    "One shared 12-frame, 90ms clock.\n\n"
    "Minting on Robinhood Chain (chain ID 4663). Gas is ETH."
)

CATEGORY_BLURBS = {
    "stage": "The room — dance floor, disco, rooftop, alley, booth, backyard, warehouse.",
    "lights": "Beat FX — spots, glints, neon, confetti, rings. Or none.",
    "cast": "Who is dancing — cats, frogs, blobs, birds, robots, and more colorways.",
    "face": "The mug on the same head points — hype, cool, wink, scream.",
    "fit": "Wear on the same groove — hoodie, shades, jacket, headphones, chain.",
    "prop": "A held extra that rides the right hand — mic, boombox, vinyl, trophy.",
}


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


def build_traits() -> None:
    TRAIT_DIR.mkdir(parents=True, exist_ok=True)
    for category, traits in TRAIT_SPEC.items():
        for trait_id, _name, _rarity in traits:
            if trait_id == "none":
                continue
            print(f"  {category}/{trait_id}")
            save_apng(render_trait_frames(category, trait_id), trait_path(category, trait_id))
    manifest = {
        "name": NAME,
        "size": SIZE,
        "frames": FRAMES,
        "durationMs": DURATION_MS,
        "format": "apng",
        "loop": 0,
        "order": list(STACK),
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Cast, face, fit, and prop share one dance clock; stage and lights move on their own loops.",
    }
    (TRAIT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def write_ts_traits() -> None:
    rows = []
    for category, traits in TRAIT_SPEC.items():
        items = []
        none_label = ""
        for trait_id, name, rarity in traits:
            if trait_id == "none":
                none_label = '    noneLabel: "None",\n'
                continue
            items.append(
                f'      {{ id: "{trait_id}", name: "{name}", image: "/{SLUG}-traits/{category}/{trait_id}.png", rarity: {rarity} }},'
            )
        rows.append(
            "  {\n"
            f'    id: "{category}",\n'
            f'    label: "{dict(TRAIT_LABELS)[category]}",\n'
            f'    blurb: "{CATEGORY_BLURBS[category]}",\n'
            f"{none_label}"
            "    traits: [\n"
            + "\n".join(items)
            + "\n    ],\n"
            "  }"
        )
    defaults = ", ".join(
        f'{category}: "{SIGNATURES[0][category]}"' for category in STACK
    )
    picks = ",\n    ".join(
        f'{category}: pick(boogieCategoryById("{category}"))' for category in STACK
    )
    stack_ids = ", ".join(f'"{c}"' for c in STACK)
    (SRC_DATA / "boogie-traits.ts").write_text(
        "export type BoogieTrait = {\n"
        "  id: string;\n"
        "  name: string;\n"
        "  image?: string;\n"
        "  rarity: number;\n"
        "};\n\n"
        "export type BoogieTraitCategory = {\n"
        f'  id: {" | ".join(chr(34) + c + chr(34) for c in STACK)};\n'
        "  label: string;\n"
        "  blurb: string;\n"
        "  noneLabel?: string;\n"
        "  traits: BoogieTrait[];\n"
        "};\n\n"
        'export const BOOGIE_ART_VERSION = "boogiesquad-v1";\n'
        f"export const BOOGIE_FRAMES = {FRAMES};\n"
        f"export const BOOGIE_DURATION_MS = {DURATION_MS};\n\n"
        "export function boogieTraitSrc(path?: string) {\n"
        "  if (!path) return \"\";\n"
        "  return `${path}?v=${BOOGIE_ART_VERSION}`;\n"
        "}\n\n"
        "export const boogieTraitCategories: BoogieTraitCategory[] = [\n"
        + ",\n".join(rows)
        + "\n];\n\n"
        'export const noneBoogieTrait: BoogieTrait = { id: "none", name: "None", rarity: 0 };\n\n'
        "export function boogieCategoryById(id: BoogieTraitCategory[\"id\"]) {\n"
        "  const category = boogieTraitCategories.find((item) => item.id === id);\n"
        "  if (!category) throw new Error(`Unknown Boogie Squad trait category: ${id}`);\n"
        "  return category;\n"
        "}\n\n"
        "export function findBoogieTrait(categoryId: BoogieTraitCategory[\"id\"], traitId: string) {\n"
        "  if (traitId === \"none\") return noneBoogieTrait;\n"
        "  return boogieCategoryById(categoryId).traits.find((trait) => trait.id === traitId);\n"
        "}\n\n"
        f"export const defaultBoogieSelection = {{\n  {defaults},\n}} as const;\n\n"
        "export type BoogieSelection = Record<BoogieTraitCategory[\"id\"], string>;\n\n"
        "export function randomBoogieSelection(): BoogieSelection {\n"
        "  const pick = (category: BoogieTraitCategory) => {\n"
        "    const pool: BoogieTrait[] = category.noneLabel\n"
        "      ? [{ id: \"none\", name: category.noneLabel, rarity: 36 }, ...category.traits]\n"
        "      : category.traits;\n"
        "    const total = pool.reduce((sum, trait) => sum + Math.max(trait.rarity, 1), 0);\n"
        "    let roll = Math.random() * total;\n"
        "    for (const trait of pool) {\n"
        "      roll -= Math.max(trait.rarity, 1);\n"
        "      if (roll <= 0) return trait.id;\n"
        "    }\n"
        "    return pool[0].id;\n"
        "  };\n"
        f"  return {{\n    {picks},\n  }};\n"
        "}\n\n"
        "export function boogieCombinationCount() {\n"
        "  return boogieTraitCategories.reduce((product, category) => {\n"
        "    const extra = category.noneLabel ? 1 : 0;\n"
        "    return product * (category.traits.length + extra);\n"
        "  }, 1);\n"
        "}\n\n"
        "export function boogieSelectionToLayers(selection: BoogieSelection) {\n"
        f"  return ([{stack_ids}] as const)\n"
        "    .map((id) => findBoogieTrait(id, selection[id]))\n"
        "    .filter((trait): trait is BoogieTrait => Boolean(trait?.image))\n"
        "    .map((trait) => boogieTraitSrc(trait.image));\n"
        "}\n",
        encoding="utf-8",
    )


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
                "name": f"{TOKEN} #{index}",
                "image": f"/{SLUG}-preview/{index}.gif",
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
    (SRC_DATA / "boogie-gallery.ts").write_text(
        "export type BoogieSample = {\n"
        "  id: number;\n"
        "  name: string;\n"
        "  image: string;\n"
        "  attributes: { trait_type: string; value: string }[];\n"
        "};\n\n"
        "export const boogieSamples: BoogieSample[] = [\n"
        + ",\n".join(rows)
        + "\n];\n",
        encoding="utf-8",
    )


def panoramic_wash(width: int, height: int) -> Image.Image:
    colors = np.array(
        [
            np.array((28, 12, 64), dtype=np.float32) / 255.0,
            np.array((255, 40, 160), dtype=np.float32) / 255.0,
            np.array((40, 220, 255), dtype=np.float32) / 255.0,
            np.array((16, 8, 36), dtype=np.float32) / 255.0,
        ],
        dtype=np.float32,
    )
    x = np.linspace(0.0, 1.0, width, dtype=np.float32)
    y = np.linspace(0.0, 1.0, height, dtype=np.float32)
    xx, yy = np.meshgrid(x, y)
    t = np.clip(xx * 0.7 + yy * 0.3, 0.0, 0.999) * (len(colors) - 1)
    i0 = np.floor(t).astype(np.int32)
    f = (t - i0)[..., None]
    c0 = colors[i0]
    c1 = colors[np.clip(i0 + 1, 0, len(colors) - 1)]
    rgb_out = c0 * (1.0 - f) + c1 * f
    arr = np.dstack([np.clip(rgb_out * 255.0, 0, 255).astype(np.uint8), np.full((height, width), 255, dtype=np.uint8)])
    return Image.fromarray(arr, "RGBA")


def write_collection_meta() -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    (META_DIR / f"{SLUG}-description.txt").write_text(COLLECTION_STORY + "\n", encoding="utf-8")
    (META_DIR / f"{SLUG}.json").write_text(
        json.dumps(
            {
                "name": NAME,
                "symbol": SYMBOL,
                "description": COLLECTION_DESCRIPTION,
                "image": f"/brand/collection-{SLUG}.gif",
                "featured_image": f"/brand/featured-{SLUG}.jpg",
                "banner_image": f"/brand/banner-{SLUG}.png",
                "opensea_banner_image": f"/brand/banner-{SLUG}-opensea.jpg",
                "external_link": f"/{SLUG}",
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
    ImageDraw.Draw(ring).ellipse((10, 10, SIZE - 10, SIZE - 10), outline=(255, 80, 180, 255), width=10)
    logo = Image.alpha_composite(logo, ring)
    save_image(logo.resize((512, 512), Image.Resampling.LANCZOS), BRAND_DIR / f"logo-{SLUG}.png")
    save_apng(
        [frame.resize((512, 512), Image.Resampling.LANCZOS) for frame in logo_frames],
        BRAND_DIR / f"logo-{SLUG}-loop.png",
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

    save_image(lineup(1500, 560, portraits[:5]).convert("RGB"), BRAND_DIR / f"banner-{SLUG}.png", quality=94)
    save_image(lineup(2800, 700, portraits).convert("RGB"), BRAND_DIR / f"banner-{SLUG}-opensea.jpg", quality=90)

    featured = panoramic_wash(1200, 800)
    place_portrait(featured, portraits[0], 90, 110, 560, radius=64)
    place_portrait(featured, portraits[3], 540, 130, 560, radius=64)
    save_image(featured.convert("RGB"), BRAND_DIR / f"featured-{SLUG}.jpg", quality=90)

    gif_frames = [frame.resize((1000, 1000), Image.Resampling.LANCZOS) for frame in logo_frames]
    save_loop_gif(gif_frames, BRAND_DIR / f"collection-{SLUG}.gif", DURATION_MS, colors=64)
    write_collection_meta()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-only", action="store_true")
    args = parser.parse_args()
    if args.brand_only:
        print("Writing Boogie Squad brand kit…")
        build_brand()
        print("Done.")
        return
    print("Building Boogie Squad jelly-cel trait loops…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
