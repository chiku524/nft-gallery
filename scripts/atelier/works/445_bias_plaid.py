"""Bias tartan. Independent salon work 445."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=445,
    slug='bias-plaid',
    title='Bias Plaid',
    description='The sett, turned until it is a new country.',
    medium='Bias tartan',
    motion='Tilt',
    palette='Cut wool',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (18, 59, 144), (237, 196, 111), (129, 185, 114), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 40, 472, 472), fill=ink)
    for n in range(8):
        mgn = 60 + n * 22
        draw.rectangle((mgn, mgn, 512 - mgn, 512 - mgn), outline=accent if n % 2 else bg, width=4)
    
    return canvas.convert("RGBA")
