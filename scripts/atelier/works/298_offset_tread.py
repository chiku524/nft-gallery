"""Offset plate. Independent salon work 298."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=298,
    slug='offset-tread',
    title='Offset Tread',
    description='The pattern missed its registration and stayed.',
    medium='Offset plate',
    motion='Shift',
    palette='Mill shift',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (93, 181, 205), (162, 74, 50), (240, 55, 171), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(10):
        y = 40 + i * 44
        for x in range(30, 480, 50):
            draw.polygon([(x, y), (x + 16, y + 8), (x, y + 16), (x - 16, y + 8)], fill=accent if i == frame % 10 else ink)
    
    return canvas.convert("RGBA")
