"""Skewings. Independent salon work 225."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=225,
    slug='skewings',
    title='Skewings',
    description='The leftovers are the luxury.',
    medium='Skewings',
    motion='Scatter',
    palette='Waste gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (103, 138, 171), (12, 12, 14), (229, 213, 100), (57, 75, 92)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((60, 60, 452, 452), fill=ink)
    crack = int(40 * math.sin(t))
    draw.line((60, 200 + crack, 452, 280 - crack), fill=bg, width=3)
    draw.line((200, 60, 260, 452), fill=bg, width=2)
    
    return canvas.convert("RGBA")
