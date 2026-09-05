"""Fountain zellige. Independent salon work 275."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=275,
    slug='fountain-rim',
    title='Fountain Rim',
    description='A rim with no water.',
    medium='Fountain zellige',
    motion='Ring',
    palette='Water tile',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (142, 234, 210), (113, 21, 45), (122, 96, 217), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(12):
        r = 20 + i * 18
        draw.regular_polygon((256, 256, r), 8, rotation=i * 8 + t * 4, outline=ink)
    
    return canvas.convert("RGBA")
