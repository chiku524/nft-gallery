"""Displaced threshold. Independent salon work 378."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=378,
    slug='displaced',
    title='Displaced',
    description='The landing moved.',
    medium='Displaced threshold',
    motion='Shift',
    palette='Arrow tarmac',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (158, 198, 192), (97, 57, 63), (34, 53, 220), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((220, 20, 292, 492), fill=mid)
    for y in range(30, 480, 36):
        draw.rectangle((246, y, 266, y + 18), fill=ink if (y // 36 + frame) % 2 else accent)
    
    return canvas.convert("RGBA")
