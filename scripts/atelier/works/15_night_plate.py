"""Astronomical plate. Magnitudes, a meridian, a sky that turns."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=15,
    slug="night-plate",
    title="Night Plate",
    description="A catalog of lights with no myth attached. The plate turns a few degrees and stops.",
    medium="Star plate",
    motion="Turn",
    palette="Navy silver",
)


def _font(size: int):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/consola.ttf", size)
    except OSError:
        return ImageFont.load_default()


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (8, 12, 28))
    draw = ImageDraw.Draw(canvas)
    rng = np.random.default_rng(77)
    xs = rng.random(90)
    ys = rng.random(90)
    mags = rng.random(90)
    rot = 0.12 * math.sin(t)
    for x, y, mag in zip(xs, ys, mags):
        px = (x - 0.5) * math.cos(rot) - (y - 0.5) * math.sin(rot)
        py = (x - 0.5) * math.sin(rot) + (y - 0.5) * math.cos(rot)
        sx, sy = int(256 + px * 420), int(256 + py * 420)
        r = 1 + int(mag * 3)
        draw.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(230, 234, 246))
    pairs = [(0, 12), (12, 33), (33, 51), (51, 8)]
    for a, b in pairs:
        draw.line(
            (
                int(256 + (xs[a] - 0.5) * 420),
                int(256 + (ys[a] - 0.5) * 420),
                int(256 + (xs[b] - 0.5) * 420),
                int(256 + (ys[b] - 0.5) * 420),
            ),
            fill=(120, 140, 180),
            width=1,
        )
    draw.ellipse((46, 46, 466, 466), outline=(168, 180, 210), width=1)
    draw.text((36, 470), "PLATE XV   RA 18h   DEC +42", font=_font(14), fill=(168, 180, 210))
    return canvas.convert("RGBA")
