"""Ramp tread. Independent salon work 148."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=148,
    slug='ramp-grip',
    title='Ramp Grip',
    description='An incline that stayed flat.',
    medium='Ramp tread',
    motion='Climb',
    palette='Safety silver',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (233, 178, 174), (22, 77, 81), (125, 121, 108), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(10):
        y = 40 + i * 44
        for x in range(30, 480, 50):
            draw.polygon([(x, y), (x + 16, y + 8), (x, y + 16), (x - 16, y + 8)], fill=accent if i == frame % 10 else ink)
    
    return canvas.convert("RGBA")
