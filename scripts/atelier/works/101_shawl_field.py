"""Paisley shawl. Independent salon work 101."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=101,
    slug='shawl-field',
    title='Shawl Field',
    description='A field of commas.',
    medium='Paisley shawl',
    motion='Drape',
    palette='Kashmir night',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (232, 193, 91), (23, 62, 164), (52, 104, 127), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.pieslice((120, 80, 360, 400), 220, 40, fill=ink)
    draw.ellipse((230, 120, 300, 190), fill=accent)
    
    return canvas.convert("RGBA")
