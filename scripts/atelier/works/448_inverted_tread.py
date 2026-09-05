"""Debossed plate. Independent salon work 448."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=448,
    slug='inverted-tread',
    title='Inverted Tread',
    description='The diamonds went in instead of out.',
    medium='Debossed plate',
    motion='Sink',
    palette='Negative steel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (83, 37, 171), (172, 218, 84), (159, 32, 68), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(10):
        y = 40 + i * 44
        for x in range(30, 480, 50):
            draw.polygon([(x, y), (x + 16, y + 8), (x, y + 16), (x - 16, y + 8)], fill=accent if i == frame % 10 else ink)
    
    return canvas.convert("RGBA")
