"""Gilt corrugate. Independent salon work 310."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=310,
    slug='gold-flute',
    title='Gold Flute',
    description='A box for nothing expensive.',
    medium='Gilt corrugate',
    motion='Flash',
    palette='Luxury kraft',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (53, 182, 178), (202, 73, 77), (239, 214, 146), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((80, 80, 432, 432), fill=mid)
    for x in range(90, 420, 14):
        draw.line((x, 90, x, 420), fill=ink, width=3)
    
    return canvas.convert("RGBA")
