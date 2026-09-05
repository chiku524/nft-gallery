"""Asanoha. Independent salon work 126."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=126,
    slug='asanoha',
    title='Asanoha',
    description='Hemp leaf, stitched.',
    medium='Asanoha',
    motion='Radiate',
    palette='Hemp indigo',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (169, 97, 195), (86, 158, 60), (66, 164, 212), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(7):
        for j in range(7):
            cx, cy = 70 + i * 60, 70 + j * 60
            for k in range(6):
                ang = k * math.tau / 6
                draw.line((cx, cy, cx + 22 * math.cos(ang), cy + 22 * math.sin(ang)), fill=ink, width=2)
    
    return canvas.convert("RGBA")
