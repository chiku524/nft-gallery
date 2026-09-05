"""Graticule figure. Independent salon work 334."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=334,
    slug='grid-scope',
    title='Grid Scope',
    description='The knot vs the furniture.',
    medium='Graticule figure',
    motion='Align',
    palette='Scope grid',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (217, 203, 28), (38, 52, 227), (50, 183, 62), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((240 + int(10 * math.sin(t)), 240, 272, 272), fill=accent)
    draw.rectangle((40, 40, 472, 472), outline=ink, width=2)
    
    return canvas.convert("RGBA")
