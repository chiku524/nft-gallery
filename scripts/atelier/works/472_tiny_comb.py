"""Microcomb. Independent salon work 472."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=472,
    slug='tiny-comb',
    title='Tiny Comb',
    description='Too small to harvest, still a field.',
    medium='Microcomb',
    motion='Pulse',
    palette='Nectar dusk',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (247, 91, 23), (8, 164, 232), (178, 102, 64), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 40, 472, 472), outline=ink, width=6)
    r = int(90 * scale)
    draw.regular_polygon((256 + ox, 256 + oy, r), 6, rotation=t * 8, fill=accent, outline=ink)
    
    return canvas.convert("RGBA")
