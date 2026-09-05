"""Tuning pin. Independent salon work 393."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=393,
    slug='tuning-pin',
    title='Tuning Pin',
    description='Hardware that is the music.',
    medium='Tuning pin',
    motion='Turn',
    palette='Pin steel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (153, 55, 40), (102, 200, 215), (153, 93, 132), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for row in range(12):
        y = 20 + row * 40
        for col in range(16):
            if (row * 3 + col + frame) % 7 == 0:
                draw.rectangle((20 + col * 30, y, 44 + col * 30, y + 16), fill=ink)
    
    return canvas.convert("RGBA")
