"""Bleached cane. Independent salon work 499."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=499,
    slug='sun-bleached',
    title='Sun Bleached',
    description='The porch won.',
    medium='Bleached cane',
    motion='Fade',
    palette='Sun cane',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (215, 83, 113), (40, 172, 142), (160, 237, 150), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(8):
        draw.arc((40 + i * 10, 80, 472 - i * 10, 432), 200, 340, fill=ink if i % 2 else accent, width=3)
    
    return canvas.convert("RGBA")
