"""Butted mail. Independent salon work 89."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=89,
    slug='butted-ring',
    title='Butted Ring',
    description='Cheap armor, honest about it.',
    medium='Butted mail',
    motion='Close',
    palette='Iron pale',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (245, 225, 148), (10, 30, 107), (140, 240, 216), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, (cx, cy) in enumerate(((180, 200), (300, 200), (240, 300), (180, 300), (300, 300))):
        r = 48 + 8 * math.sin(t + i)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ink, width=8)
        draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=accent)
    
    return canvas.convert("RGBA")
