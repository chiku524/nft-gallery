"""Thick figure. Independent salon work 274."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=274,
    slug='fat-trace',
    title='Fat Trace',
    description='A knot drawn with a tired beam.',
    medium='Thick figure',
    motion='Glow',
    palette='Bloom gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (97, 75, 185), (158, 180, 70), (92, 163, 143), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((96, 96, 416, 416), outline=ink, width=6)
    
    return canvas.convert("RGBA")
