"""Gilt contour. Independent salon work 398."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=398,
    slug='gold-survey',
    title='Gold Survey',
    description='A luxury map of nothing.',
    medium='Gilt contour',
    motion='Trace',
    palette='Gilt map',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (178, 16, 173), (77, 239, 82), (92, 130, 211), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(10):
        r = int((30 + i * 20) * scale)
        draw.ellipse((256 - r + ox, 256 - r + oy, 256 + r + ox, 256 + r + oy), outline=ink, width=2 + (i % 5 == 0) * 2)
    
    return canvas.convert("RGBA")
