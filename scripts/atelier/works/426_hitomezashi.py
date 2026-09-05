"""Hitomezashi. Independent salon work 426."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=426,
    slug='hitomezashi',
    title='Hitomezashi',
    description='Counted, then crossed.',
    medium='Hitomezashi',
    motion='Count',
    palette='Grid stitch',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (105, 126, 128), (244, 240, 232), (153, 203, 205), (174, 183, 180)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(7):
        for j in range(7):
            cx, cy = 70 + i * 60, 70 + j * 60
            for k in range(6):
                ang = k * math.tau / 6
                draw.line((cx, cy, cx + 22 * math.cos(ang), cy + 22 * math.sin(ang)), fill=ink, width=2)
    
    return canvas.convert("RGBA")
