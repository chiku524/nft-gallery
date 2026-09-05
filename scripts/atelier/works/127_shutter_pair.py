"""Plantation shutter. Independent salon work 127."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=127,
    slug='shutter-pair',
    title='Shutter Pair',
    description='A porch without a house.',
    medium='Plantation shutter',
    motion='Fold',
    palette='Porch white',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (50, 139, 211), (205, 116, 44), (196, 96, 166), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((80, 40, 432, 472), outline=ink, width=10)
    for y in range(70, 450, 24):
        draw.rectangle((100, y, 412, y + 10), fill=accent)
    
    return canvas.convert("RGBA")
