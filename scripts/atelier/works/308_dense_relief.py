"""Dense contour. Independent salon work 308."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=308,
    slug='dense-relief',
    title='Dense Relief',
    description='The hill is almost black with trying.',
    medium='Dense contour',
    motion='Crowd',
    palette='Steep brown',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (142, 119, 105), (244, 240, 232), (101, 238, 134), (193, 179, 168)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((80, 400, 200, 180, 320, 260, 430, 90), fill=ink, width=6)
    draw.regular_polygon((430, 90, 8), 3, fill=accent)
    
    return canvas.convert("RGBA")
