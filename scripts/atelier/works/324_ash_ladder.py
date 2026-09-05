"""Ash strip. Independent salon work 324."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=324,
    slug='ash-ladder',
    title='Ash Ladder',
    description='Rungs without a climb.',
    medium='Ash strip',
    motion='Rise',
    palette='Pale ash',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (183, 147, 141), (12, 12, 14), (124, 157, 158), (97, 79, 77)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((48, 48, 464, 464), outline=ink, width=10)
    for i in range(6):
        x = 80 + i * 60
        draw.polygon([(x, 140), (x + 40, 200), (x + 40, 360), (x, 300)], fill=accent if i == frame % 6 else ink)
    
    return canvas.convert("RGBA")
