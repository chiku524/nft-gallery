"""Single leaf. Independent salon work 195."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=195,
    slug='one-square',
    title='One Square',
    description='One book of gold, one page.',
    medium='Single leaf',
    motion='Seat',
    palette='Lone gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (35, 28, 167), (220, 227, 88), (188, 146, 238), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 40, 472, 472), outline=ink, width=20)
    draw.rectangle((80, 80, 432, 432), fill=accent)
    
    return canvas.convert("RGBA")
