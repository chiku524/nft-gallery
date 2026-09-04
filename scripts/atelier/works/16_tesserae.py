"""Mosaic. Irregular tiles, grout, a highlight that walks."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=16,
    slug="tesserae",
    title="Tesserae",
    description="A wall of glass squares with no picture in mind. Light crosses them anyway.",
    medium="Glass mosaic",
    motion="Gleam",
    palette="Grout jewel",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (42, 40, 38))
    draw = ImageDraw.Draw(canvas)
    rng = np.random.default_rng(16)
    palette = [
        (168, 42, 48),
        (36, 86, 120),
        (214, 176, 72),
        (48, 110, 78),
        (196, 98, 64),
        (92, 72, 128),
        (230, 220, 200),
    ]
    gleam_x = 256 + 180 * math.cos(t)
    gleam_y = 256 + 140 * math.sin(t)
    for row in range(16):
        for col in range(16):
            jx = int(rng.integers(-3, 4))
            jy = int(rng.integers(-3, 4))
            x0 = 16 + col * 30 + jx
            y0 = 16 + row * 30 + jy
            color = palette[(row * 3 + col) % len(palette)]
            d = math.hypot(x0 - gleam_x, y0 - gleam_y)
            if d < 70:
                color = tuple(min(255, int(c + 70 * (1 - d / 70))) for c in color)
            draw.rectangle((x0, y0, x0 + 24, y0 + 24), fill=color)
    return canvas.convert("RGBA")
