"""Parade mail. Independent salon work 479."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=479,
    slug='ceremonial',
    title='Ceremonial',
    description='Too bright to hide in.',
    medium='Parade mail',
    motion='Shine',
    palette='Parade silver',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (32, 191, 57), (223, 64, 198), (231, 134, 22), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(6):
        x = 70 + i * 70
        draw.ellipse((x, 180, x + 64, 360), outline=ink if i % 2 else accent, width=5)
    
    return canvas.convert("RGBA")
