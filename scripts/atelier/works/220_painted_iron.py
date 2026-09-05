"""Painted corrugate. Independent salon work 220."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=220,
    slug='painted-iron',
    title='Painted Iron',
    description='A barn that is only its skin.',
    medium='Painted corrugate',
    motion='Coat',
    palette='Barn red',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (223, 175, 219), (32, 80, 36), (83, 73, 205), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for x in range(0, 512, int(18 * scale)):
        draw.polygon([(x, 0), (x + 8, 0), (x + 8, 512), (x, 512)], fill=ink if (x // 18) % 2 else accent)
    
    return canvas.convert("RGBA")
