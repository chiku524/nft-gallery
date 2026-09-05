"""Closed contour. Independent salon work 98."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=98,
    slug='closed-loop',
    title='Closed Loop',
    description='A summit that is only a sentence.',
    medium='Closed contour',
    motion='Nest',
    palette='Map umber',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (153, 73, 231), (102, 182, 24), (135, 162, 159), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(10):
        r = int((30 + i * 20) * scale)
        draw.ellipse((256 - r + ox, 256 - r + oy, 256 + r + ox, 256 + r + oy), outline=ink, width=2 + (i % 5 == 0) * 2)
    
    return canvas.convert("RGBA")
