"""Clinker row. Independent salon work 323."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=323,
    slug='clinker',
    title='Clinker',
    description='A hull that forgot the water.',
    medium='Clinker row',
    motion='Overlap',
    palette='Boat tar',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (156, 62, 205), (99, 193, 50), (130, 66, 186), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((60, 80, 450, 470), outline=ink, width=8)
    for y in range(120, 420, int(36 * scale)):
        for x in range(100, 400, 40):
            draw.chord((x, y, x + 34, y + 24), 210, 330, fill=accent)
    
    return canvas.convert("RGBA")
