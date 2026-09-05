"""Index contour. Independent salon work 158."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=158,
    slug='index-contour',
    title='Index Contour',
    description='Every fifth line speaks up.',
    medium='Index contour',
    motion='Bold',
    palette='Survey ink',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (58, 109, 149), (244, 240, 232), (25, 181, 184), (151, 174, 190)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((80, 400, 200, 180, 320, 260, 430, 90), fill=ink, width=6)
    draw.regular_polygon((430, 90, 8), 3, fill=accent)
    
    return canvas.convert("RGBA")
