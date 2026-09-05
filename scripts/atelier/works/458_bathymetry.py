"""Bathymetry. Independent salon work 458."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=458,
    slug='bathymetry',
    title='Bathymetry',
    description='Down, not up.',
    medium='Bathymetry',
    motion='Deep',
    palette='Ocean ink',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (219, 110, 118), (36, 145, 137), (235, 150, 86), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((80, 400, 200, 180, 320, 260, 430, 90), fill=ink, width=6)
    draw.regular_polygon((430, 90, 8), 3, fill=accent)
    
    return canvas.convert("RGBA")
