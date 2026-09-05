"""Runway paint. Independent salon work 78."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=78,
    slug='centerline',
    title='Centerline',
    description='A landing that does not happen.',
    medium='Runway paint',
    motion='Aim',
    palette='Tarmac yellow',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (143, 171, 205), (112, 84, 50), (62, 229, 95), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((220, 20, 292, 492), fill=mid)
    for y in range(30, 480, 36):
        draw.rectangle((246, y, 266, y + 18), fill=ink if (y // 36 + frame) % 2 else accent)
    
    return canvas.convert("RGBA")
