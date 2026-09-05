"""Spot height. Independent salon work 188."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=188,
    slug='spot-height',
    title='Spot Height',
    description='A number that forgot its digits.',
    medium='Spot height',
    motion='Mark',
    palette='Triangle brown',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (130, 183, 38), (125, 72, 217), (238, 223, 192), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(6):
        r = 50 + i * 30
        draw.ellipse((256 - r, 256 - r, 256 + r, 256 + r), outline=accent if i == frame % 6 else ink, width=3)
    
    return canvas.convert("RGBA")
