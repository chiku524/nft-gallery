"""Negative paisley. Independent salon work 251."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=251,
    slug='inverted',
    title='Inverted Boteh',
    description='The comma as a hole.',
    medium='Negative paisley',
    motion='Flip',
    palette='Void dye',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (133, 228, 220), (122, 27, 35), (75, 87, 232), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.pieslice((120, 80, 360, 400), 220, 40, fill=ink)
    draw.ellipse((230, 120, 300, 190), fill=accent)
    
    return canvas.convert("RGBA")
