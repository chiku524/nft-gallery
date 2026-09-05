"""Crushed flute. Independent salon work 340."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=340,
    slug='crushed',
    title='Crushed',
    description='The cushion lost.',
    medium='Crushed flute',
    motion='Fail',
    palette='Damaged kraft',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (189, 99, 244), (66, 156, 11), (185, 141, 210), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(8):
        x = 40 + i * 56
        draw.arc((x, 80, x + 56, 432), 270, 90, fill=ink if i % 2 else accent, width=8)
    
    return canvas.convert("RGBA")
