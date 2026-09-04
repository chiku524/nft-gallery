#!/usr/bin/env python3
"""Paint Groovy Nation — clip-art musical-note mascots.

Every trait is a 12-frame APNG on a shared 512 canvas and 90ms clock.
Note, expression, topper, and cable share one bounce so faces stay on the head.
Venue stays a stage. Riff floats on its own pulse.

Look: cartoon notation. Round notehead is the face. Black stem goes up.
Flag or beam at the top. Stick arms and legs dance. Bold outline, flat fill.
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

INK = (20, 18, 24, 255)
WHITE = (255, 255, 255, 255)
TONGUE = (236, 118, 148, 255)
STROKE = 8
LIMB = 7

CX = 248.0
HEAD_Y = 272.0
HEAD_R = 90.0
STEM_LEN = 132.0
STEM_W = 16

VENUES = ("sunset", "lava", "checker", "velvet", "blacklight", "chrome")
NOTES = ("quarter", "eighth", "whole", "beamed")
EXPRESSIONS = ("cool", "shout", "wink", "groove", "star")
TOPPERS = ("none", "afro", "shades", "visor", "halo")
CABLES = ("none", "chain", "cans", "mic")
RIFFS = ("none", "treble", "vinyl", "stars", "bolt")

NOTE_FILL = {
    "quarter": (86, 102, 128, 255),
    "eighth": (196, 62, 118, 255),
    "whole": (240, 236, 246, 255),
    "beamed": (42, 168, 158, 255),
}


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def beat(frame: int) -> tuple[float, float]:
    t = frame / FRAMES * math.tau
    return -abs(math.sin(t)) * 10.0, math.sin(t)


def head_xy(frame: int) -> tuple[float, float]:
    dy, _swing = beat(frame)
    return CX, HEAD_Y + dy


def stem_xy(hx: float, hy: float) -> tuple[float, float, float, float]:
    sx = hx + HEAD_R * 0.62
    sy = hy - HEAD_R * 0.42
    return sx, sy, sx + 3.0, sy - STEM_LEN


def layout(frame: int) -> dict[str, float | tuple[float, float]]:
    """Shared seat for face, hats, and cables on the cartoon notehead."""
    hx, hy = head_xy(frame)
    _dy, swing = beat(frame)
    ey = hy - HEAD_R * 0.40
    sl = (hx - HEAD_R * 0.92, hy + 10)
    la = (sl[0] - 38 - swing * 10, sl[1] - 52 + swing * 34)
    return {
        "hx": hx,
        "hy": hy,
        "swing": swing,
        "lx": hx - 30,
        "rx": hx + 30,
        "ey": ey,
        "mouth_y": hy + 20,
        "crown": hy - HEAD_R,
        "chin": hy + HEAD_R,
        "ear_l": (hx - HEAD_R - 10, hy - 28),
        "ear_r": (hx + HEAD_R + 10, hy - 28),
        "hand_l": la,
    }


def draw_line(draw: ImageDraw.ImageDraw, a: tuple[float, float], b: tuple[float, float], fill=INK, width: int = LIMB) -> None:
    draw.line((a[0], a[1], b[0], b[1]), fill=fill, width=width, joint="curve")
    r = max(width // 2, 2)
    draw.ellipse((a[0] - r, a[1] - r, a[0] + r, a[1] + r), fill=fill)
    draw.ellipse((b[0] - r, b[1] - r, b[0] + r, b[1] + r), fill=fill)


def draw_circle(draw: ImageDraw.ImageDraw, x: float, y: float, r: float, fill, outline=INK, width: int = STROKE) -> None:
    draw.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=outline, width=width)


def draw_staff(draw: ImageDraw.ImageDraw, color: tuple[int, int, int, int], width: int = 3) -> None:
    for i in range(5):
        y = 214 + i * 26
        draw.line((48, y, 464, y), fill=color, width=width)


def paint_venue(kind: str, frame: int) -> Image.Image:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if kind == "sunset":
        for y in range(SIZE):
            t = y / (SIZE - 1)
            r = int(255 * (1.0 - t * 0.15) + 210 * t)
            g = int(140 * (1.0 - t) + 48 * t)
            b = int(72 * (1.0 - t) + 150 * t)
            draw.line((0, y, SIZE, y), fill=(r, g, b, 255))
        draw.ellipse((36, 28, 196, 188), fill=(255, 214, 96, 255), outline=INK, width=6)
        draw_staff(draw, (48, 22, 36, 180), 3)
    elif kind == "lava":
        draw.rectangle((0, 0, SIZE, SIZE), fill=(28, 12, 42, 255))
        blobs = ((90, 120, 70, (220, 56, 140, 255)), (360, 200, 86, (48, 196, 186, 255)), (230, 400, 100, (240, 140, 48, 255)))
        phase = frame / FRAMES * math.tau
        for bx, by, br, col in blobs:
            ox = math.sin(phase + bx) * 10
            oy = math.cos(phase + by) * 8
            draw.ellipse((bx + ox - br, by + oy - br, bx + ox + br, by + oy + br), fill=col, outline=INK, width=5)
        draw_staff(draw, (255, 230, 200, 90), 3)
    elif kind == "checker":
        draw.rectangle((0, 0, SIZE, SIZE), fill=(42, 16, 58, 255))
        cell = 48
        for row in range(7, 12):
            for col in range(11):
                if (row + col) % 2 == 0:
                    x0, y0 = col * cell, row * cell
                    draw.rectangle((x0, y0, x0 + cell, y0 + cell), fill=(244, 196, 64, 255))
        draw_staff(draw, (255, 230, 180, 70), 3)
    elif kind == "velvet":
        draw.rectangle((0, 0, SIZE, SIZE), fill=(72, 16, 48, 255))
        draw.ellipse((90, 80, 422, 420), fill=(110, 28, 68, 255), outline=INK, width=6)
        draw_staff(draw, (255, 210, 220, 80), 3)
    elif kind == "blacklight":
        draw.rectangle((0, 0, SIZE, SIZE), fill=(12, 28, 40, 255))
        for i in range(14):
            px = 40 + (i * 97) % 430
            py = 40 + (i * 53) % 400 + int(math.sin(frame / FRAMES * math.tau + i) * 6)
            col = (72, 230, 140, 255) if i % 2 else (196, 80, 230, 255)
            draw.ellipse((px - 8, py - 8, px + 8, py + 8), fill=col, outline=INK, width=3)
        draw_staff(draw, (180, 255, 210, 80), 3)
    else:
        draw.rectangle((0, 0, SIZE, SIZE), fill=(186, 194, 210, 255))
        draw.ellipse((150, 428, 370, 488), fill=(230, 236, 246, 120))
        draw_staff(draw, (40, 40, 52, 160), 3)
    return img


def draw_limbs(draw: ImageDraw.ImageDraw, hx: float, hy: float, swing: float) -> None:
    sl = (hx - HEAD_R * 0.92, hy + 10)
    sr = (hx + HEAD_R * 0.92, hy + 10)
    la = (sl[0] - 38 - swing * 10, sl[1] - 52 + swing * 34)
    ra = (sr[0] + 30 + swing * 12, sr[1] + 18 - swing * 42)
    draw_line(draw, sl, la)
    draw_line(draw, sr, ra)
    # pointing fingers
    draw_line(draw, la, (la[0] - 6, la[1] - 22), width=5)
    draw_line(draw, ra, (ra[0] + 18, ra[1] + 4), width=5)

    hl = (hx - 24, hy + HEAD_R * 0.86)
    hr = (hx + 24, hy + HEAD_R * 0.86)
    lf = (hl[0] - 6 + swing * 24, hl[1] + 78)
    rf = (hr[0] + 4 - swing * 18, hr[1] + 72 + abs(swing) * 6)
    lk = ((hl[0] + lf[0]) * 0.5 - 8, (hl[1] + lf[1]) * 0.5)
    rk = ((hr[0] + rf[0]) * 0.5 + 6, (hr[1] + rf[1]) * 0.5)
    draw_line(draw, hl, lk)
    draw_line(draw, lk, lf)
    draw_line(draw, hr, rk)
    draw_line(draw, rk, rf)
    draw.ellipse((lf[0] - 18, lf[1] - 8, lf[0] + 20, lf[1] + 10), fill=INK)
    draw.ellipse((rf[0] - 18, rf[1] - 8, rf[0] + 20, rf[1] + 10), fill=INK)


def draw_flag(draw: ImageDraw.ImageDraw, tx: float, ty: float) -> None:
    pts = [
        (tx - 1, ty),
        (tx + 18, ty + 4),
        (tx + 74, ty + 14),
        (tx + 92, ty + 42),
        (tx + 78, ty + 88),
        (tx + 48, ty + 52),
        (tx + 16, ty + 30),
        (tx + 2, ty + 22),
    ]
    draw.polygon(pts, fill=INK)


def draw_notehead(draw: ImageDraw.ImageDraw, hx: float, hy: float, fill, hollow: bool = False) -> None:
    if hollow:
        draw_circle(draw, hx, hy, HEAD_R, WHITE)
        draw_circle(draw, hx, hy, HEAD_R, None, INK, STROKE + 6)
        draw_circle(draw, hx, hy, HEAD_R - 16, None, INK, 14)
    else:
        draw_circle(draw, hx, hy, HEAD_R, fill)
        draw.ellipse((hx - 52, hy - 72, hx - 12, hy - 40), fill=(255, 255, 255, 55))


def paint_note(kind: str, frame: int) -> Image.Image:
    img = blank()
    draw = ImageDraw.Draw(img)
    hx, hy = head_xy(frame)
    _dy, swing = beat(frame)
    fill = NOTE_FILL[kind]
    sx, sy, tx, ty = stem_xy(hx, hy)

    draw.ellipse((hx - 74, hy + HEAD_R + 78, hx + 80, hy + HEAD_R + 98), fill=(20, 18, 24, 46))
    draw_limbs(draw, hx, hy, swing)

    if kind != "whole":
        draw_line(draw, (sx, sy), (tx, ty), INK, STEM_W)

    if kind == "eighth":
        draw_flag(draw, tx, ty)
    elif kind == "beamed":
        hx2, hy2 = hx + 128, hy + 16
        sx2, sy2, tx2, ty2 = stem_xy(hx2, hy2)
        draw_line(draw, (sx2, sy2), (tx2, ty2), INK, STEM_W)
        draw.polygon(
            [(tx - 4, ty + 2), (tx2 + 6, ty2 + 2), (tx2 + 6, ty2 + 24), (tx - 4, ty + 24)],
            fill=INK,
        )
        draw.polygon(
            [(tx - 4, ty + 34), (tx2 + 6, ty2 + 34), (tx2 + 6, ty2 + 50), (tx - 4, ty + 50)],
            fill=INK,
        )
        draw_notehead(draw, hx2, hy2, fill)

    draw_notehead(draw, hx, hy, fill, hollow=(kind == "whole"))
    return img


def paint_expression(kind: str, frame: int) -> Image.Image:
    img = blank()
    draw = ImageDraw.Draw(img)
    seat = layout(frame)
    hx, hy = float(seat["hx"]), float(seat["hy"])
    lx, rx, ey = float(seat["lx"]), float(seat["rx"]), float(seat["ey"])
    mouth_y = float(seat["mouth_y"])
    blink = frame in (5, 6)

    def open_eye(x: float, y: float, pupil: tuple[int, int, int, int] = (28, 46, 140, 255)) -> None:
        draw_circle(draw, x, y, 20, WHITE, INK, 5)
        draw_circle(draw, x + 4, y + 2, 7, pupil, INK, 2)
        draw.ellipse((x - 9, y - 11, x - 2, y - 4), fill=WHITE)

    def shut_eye(x: float, y: float) -> None:
        draw.arc((x - 18, y - 8, x + 18, y + 12), 200, 340, fill=INK, width=6)

    def cool_eye(x: float, y: float) -> None:
        draw_circle(draw, x, y, 20, WHITE, INK, 5)
        draw.pieslice((x - 20, y - 20, x + 20, y + 8), 200, 340, fill=INK)
        draw_circle(draw, x + 3, y + 6, 5, (28, 46, 140, 255), INK, 2)

    def brows(angle: float = -8) -> None:
        draw.arc((lx - 20, ey - 32, lx + 16, ey - 4), 200 + angle, 340 + angle, fill=INK, width=6)
        draw.arc((rx - 16, ey - 32, rx + 20, ey - 4), 200 - angle, 340 - angle, fill=INK, width=6)

    if kind == "cool":
        brows(12)
        if blink:
            shut_eye(lx, ey)
            shut_eye(rx, ey)
        else:
            cool_eye(lx, ey)
            cool_eye(rx, ey)
        draw.arc((hx - 22, mouth_y - 6, hx + 28, mouth_y + 28), 10, 160, fill=INK, width=6)
    elif kind == "shout":
        brows(-16)
        if blink:
            shut_eye(lx, ey)
            shut_eye(rx, ey)
        else:
            open_eye(lx, ey)
            open_eye(rx, ey)
        draw.ellipse((hx - 34, mouth_y - 18, hx + 34, mouth_y + 38), fill=INK, outline=INK, width=4)
        draw.ellipse((hx - 14, mouth_y + 8, hx + 14, mouth_y + 34), fill=TONGUE)
    elif kind == "wink":
        brows(6)
        shut_eye(lx, ey)
        if blink:
            shut_eye(rx, ey)
        else:
            open_eye(rx, ey)
        draw.arc((hx - 22, mouth_y - 4, hx + 28, mouth_y + 28), 10, 170, fill=INK, width=6)
    elif kind == "groove":
        brows(0)
        shut_eye(lx, ey + 2)
        shut_eye(rx, ey + 2)
        draw.arc((hx - 30, mouth_y - 8, hx + 30, mouth_y + 32), 10, 170, fill=INK, width=7)
    else:
        brows(4)
        if blink:
            shut_eye(lx, ey)
            shut_eye(rx, ey)
        else:
            open_eye(lx, ey, (236, 168, 40, 255))
            open_eye(rx, ey, (236, 168, 40, 255))
            for x in (lx, rx):
                draw.line((x - 11, ey, x + 11, ey), fill=(255, 214, 80, 255), width=3)
                draw.line((x, ey - 11, x, ey + 11), fill=(255, 214, 80, 255), width=3)
        draw.ellipse((hx - 12, mouth_y, hx + 12, mouth_y + 22), fill=TONGUE, outline=INK, width=4)
    return img


def paint_topper(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    img = blank()
    draw = ImageDraw.Draw(img)
    seat = layout(frame)
    hx, hy = float(seat["hx"]), float(seat["hy"])
    ey = float(seat["ey"])
    crown = float(seat["crown"])
    if kind == "afro":
        for ox, oy, r in ((-42, -86, 46), (42, -88, 46), (0, -108, 52), (-68, -52, 36), (68, -54, 36)):
            draw_circle(draw, hx + ox, hy + oy, r, (92, 48, 24, 255), INK, 6)
    elif kind == "shades":
        draw.rounded_rectangle((hx - 62, ey - 22, hx + 62, ey + 22), radius=14, fill=INK)
        draw.ellipse((hx - 48, ey - 16, hx - 8, ey + 16), fill=(48, 42, 56, 255))
        draw.ellipse((hx + 8, ey - 16, hx + 48, ey + 16), fill=(48, 42, 56, 255))
        draw.line((hx - 40, ey - 8, hx - 18, ey + 2), fill=(255, 220, 90, 255), width=3)
    elif kind == "visor":
        knit = (244, 186, 64, 255)
        cuff = (196, 128, 40, 255)
        rib = (176, 108, 28, 255)
        draw.ellipse((hx - 54, crown - 50, hx + 38, crown + 14), fill=knit, outline=INK, width=STROKE)
        draw.arc((hx - 40, crown - 46, hx + 6, crown + 2), 200, 340, fill=rib, width=4)
        draw.arc((hx - 14, crown - 46, hx + 26, crown + 2), 200, 340, fill=rib, width=4)
        r_cuff = HEAD_R + 6
        draw.arc((hx - r_cuff, hy - r_cuff, hx + r_cuff, hy + r_cuff), 205, 330, fill=INK, width=20)
        draw.arc((hx - r_cuff, hy - r_cuff, hx + r_cuff, hy + r_cuff), 205, 330, fill=cuff, width=12)
        draw_circle(draw, hx - 6, crown - 52, 13, (255, 236, 200, 255))
    else:
        draw.ellipse((hx - 46, crown - 64, hx + 34, crown - 20), outline=(255, 206, 64, 255), width=12)
        draw.ellipse((hx - 46, crown - 64, hx + 34, crown - 20), outline=INK, width=4)
    return img


def paint_cable(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    img = blank()
    draw = ImageDraw.Draw(img)
    seat = layout(frame)
    hx, hy = float(seat["hx"]), float(seat["hy"])
    crown = float(seat["crown"])
    chin = float(seat["chin"])
    if kind == "chain":
        gold = (240, 186, 48, 255)
        for t in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
            px = hx - 52 + 104 * t
            py = chin - 18 + math.sin(t * math.pi) * 26
            draw.ellipse((px - 13, py - 13, px + 13, py + 13), outline=gold, width=6)
            draw.ellipse((px - 13, py - 13, px + 13, py + 13), outline=INK, width=2)
    elif kind == "cans":
        el = seat["ear_l"]
        er = seat["ear_r"]
        assert isinstance(el, tuple) and isinstance(er, tuple)
        draw.arc((el[0] - 4, crown - 22, er[0] + 4, hy + 10), 200, 340, fill=INK, width=14)
        for ex, ey in (el, er):
            draw_circle(draw, ex, ey, 30, INK)
            draw_circle(draw, ex, ey, 24, (220, 224, 234, 255), INK, 4)
            draw_circle(draw, ex, ey, 10, (48, 24, 36, 255), INK, 3)
    else:
        hand = seat["hand_l"]
        assert isinstance(hand, tuple)
        mx, my = hand[0] + 2, hand[1] - 22
        draw.line((mx, my + 16, mx - 8, my + 78), fill=INK, width=16)
        draw_circle(draw, mx + 4, my - 6, 26, INK)
        draw_circle(draw, mx + 4, my - 6, 21, (168, 174, 186, 255), INK, 4)
        for gy in (-10, -2, 6):
            draw.line((mx - 8, my - 6 + gy, mx + 16, my - 6 + gy), fill=(52, 48, 58, 255), width=2)
        draw_circle(draw, mx + 4, my - 6, 6, (32, 28, 36, 255), INK, 2)
    return img


def paint_riff(kind: str, frame: int) -> Image.Image:
    if kind == "none":
        return blank()
    img = blank()
    draw = ImageDraw.Draw(img)
    t = frame / FRAMES * math.tau
    ox, oy = math.sin(t) * 8, math.cos(t * 1.2) * 10
    if kind == "treble":
        x, y = 454 + ox, 118 + oy
        draw.arc((x - 18, y - 40, x + 28, y + 8), 200, 40, fill=(240, 186, 48, 255), width=8)
        draw.arc((x - 22, y, x + 24, y + 48), 20, 200, fill=(240, 186, 48, 255), width=8)
        draw_circle(draw, x + 4, y + 58, 8, (240, 186, 48, 255), INK, 3)
    elif kind == "vinyl":
        x, y = 56 + ox * 0.3, 52 + oy * 0.3
        draw_circle(draw, x, y, 30, INK)
        draw_circle(draw, x, y, 18, (60, 56, 64, 255), INK, 3)
        draw_circle(draw, x, y, 7, (220, 64, 130, 255), INK, 3)
    elif kind == "stars":
        for i, (x, y) in enumerate(((48, 42), (464, 48), (468, 248), (36, 268))):
            s = 8 + 4 * abs(math.sin(t + i))
            draw.polygon(
                [(x, y - s * 1.6), (x + s * 0.4, y - s * 0.2), (x + s * 1.4, y), (x + s * 0.4, y + s * 0.2), (x, y + s * 1.6), (x - s * 0.4, y + s * 0.2), (x - s * 1.4, y), (x - s * 0.4, y - s * 0.2)],
                fill=(255, 214, 80, 255),
                outline=INK,
            )
    else:
        x, y = 448 + ox, 292 + oy
        draw.polygon(
            [(x, y - 36), (x + 22, y - 8), (x + 4, y - 4), (x + 28, y + 40), (x + 2, y + 10), (x + 16, y + 6)],
            fill=(255, 214, 64, 255),
            outline=INK,
        )
    return img


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
        ("visor", "Beanie", 16),
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
    "then flattened onto one 12-frame GIF. Clip-art note mascots: round heads, black stems, dancing stick limbs."
)

COLLECTION_STORY = (
    "Welcome to Groovy Nation.\n\n"
    "An 8,888-piece collection of looping musical-note PFP GIFs on Robinhood Chain. "
    "Each citizen is stacked from six layers — venue, note, expression, topper, cable, and riff — "
    "then flattened onto one 12-frame GIF. The notehead is the face. A black stem goes up. "
    "Flags and beams sit at the top. Stick arms and legs dance on the beat.\n\n"
    "Four notes only: quarter, eighth, whole, and beamed. Bold outline, flat fill, cartoon notation. "
    "Shades sit on the head. Chains hang on the chin. Riffs float beside the beat. One shared clock.\n\n"
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
        "note": "Each trait is a looping APNG. Studio stacks them live. Minted tokens flatten to GIF. Cartoon note mascots share one bounce; toppers, cables, and riffs never edit the note.",
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
            f'    image: "{sample["image"]}?v=5",\n'
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
    ImageDraw.Draw(ring).ellipse((10, 10, SIZE - 10, SIZE - 10), outline=(20, 18, 24, 255), width=10)
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
    print("Building Groovy Nation clip-art note mascots…")
    build_traits()
    print("Compositing sample GIF tokens…")
    build_samples()
    print("Writing brand…")
    build_brand()
    print("Done.")


if __name__ == "__main__":
    main()
