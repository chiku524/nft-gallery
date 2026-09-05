"""Wood louver. Independent salon work 427."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=427,
    slug='wood-louver',
    title='Wood Louver',
    description='Furniture that used to be a tree’s privacy.',
    medium='Wood louver',
    motion='Breathe',
    palette='Teak slat',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (165, 98, 114), (244, 240, 232), (42, 211, 100), (204, 169, 173)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((80, 40, 432, 472), outline=ink, width=10)
    for y in range(70, 450, 24):
        draw.rectangle((100, y, 412, y + 10), fill=accent)
    
    return canvas.convert("RGBA")
