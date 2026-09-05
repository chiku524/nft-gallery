"""Hex nut. Independent salon work 202."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=202,
    slug='nut-plate',
    title='Nut Plate',
    description='Threaded air.',
    medium='Hex nut',
    motion='Seat',
    palette='Cadmium shop',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (150, 189, 209), (105, 66, 46), (176, 67, 105), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    s = int(22 * scale)
    for row in range(-2, 16):
        for col in range(-2, 16):
            cx = 40 + col * s * 1.75 + (row % 2) * s * 0.88 + 8 * math.cos(t + row)
            cy = 36 + row * s * 1.5
            r = s * 0.62
            pts = [(cx + r * math.cos(k * math.tau / 6 + spin), cy + r * math.sin(k * math.tau / 6 + spin)) for k in range(6)]
            draw.polygon([(int(x), int(y)) for x, y in pts], outline=ink, width=2)
    
    return canvas.convert("RGBA")
