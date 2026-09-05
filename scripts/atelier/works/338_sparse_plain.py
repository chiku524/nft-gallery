"""Sparse contour. Independent salon work 338."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=338,
    slug='sparse-plain',
    title='Sparse Plain',
    description='Almost no news.',
    medium='Sparse contour',
    motion='Rest',
    palette='Plain cream',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (221, 45, 93), (34, 210, 162), (152, 22, 185), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(6):
        r = 50 + i * 30
        draw.ellipse((256 - r, 256 - r, 256 + r, 256 + r), outline=accent if i == frame % 6 else ink, width=3)
    
    return canvas.convert("RGBA")
