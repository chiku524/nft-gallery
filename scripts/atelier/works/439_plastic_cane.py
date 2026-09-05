"""Plastic cane. Independent salon work 439."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=439,
    slug='plastic-cane',
    title='Plastic Cane',
    description='A porch that never was vine.',
    medium='Plastic cane',
    motion='Fake',
    palette='Patio white',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (197, 101, 39), (58, 154, 216), (150, 224, 128), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((80, 80, 432, 432), outline=ink, width=8)
    draw.ellipse((160, 160, 352, 352), outline=accent, width=6)
    
    return canvas.convert("RGBA")
