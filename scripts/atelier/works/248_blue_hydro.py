"""Hydrography. Independent salon work 248."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=248,
    slug='blue-hydro',
    title='Blue Hydro',
    description='Water as a law.',
    medium='Hydrography',
    motion='Flow',
    palette='River cyan',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (12, 245, 85), (243, 10, 170), (99, 160, 123), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(10):
        r = int((30 + i * 20) * scale)
        draw.ellipse((256 - r + ox, 256 - r + oy, 256 + r + ox, 256 + r + oy), outline=ink, width=2 + (i % 5 == 0) * 2)
    
    return canvas.convert("RGBA")
