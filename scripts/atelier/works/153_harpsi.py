"""Harpsichord key. Independent salon work 153."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=153,
    slug='harpsi',
    title='Harpsi',
    description='A different attack, same furniture.',
    medium='Harpsichord key',
    motion='Pluck',
    palette='Gilt cream',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (153, 231, 54), (102, 24, 201), (179, 26, 117), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((80, 200, 432, 280), fill=mid, outline=ink, width=6)
    draw.ellipse((220, 210, 300, 270), fill=accent)
    
    return canvas.convert("RGBA")
