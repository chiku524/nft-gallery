"""Terrazzo strip. Independent salon work 117."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=117,
    slug='brass-divider',
    title='Brass Divider',
    description='The divider is the drawing.',
    medium='Terrazzo strip',
    motion='Bound',
    palette='Brass mint',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (150, 155, 56), (105, 100, 199), (73, 189, 65), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(12):
        x = 30 + (i * 41 + frame * 7) % 450
        y = 40 + (i * 73) % 420
        draw.regular_polygon((x, y, 18), 3 + (i % 3), fill=accent if i % 2 else ink)
    
    return canvas.convert("RGBA")
