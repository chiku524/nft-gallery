"""Burnished leaf. Independent salon work 345."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=345,
    slug='burnish-spot',
    title='Burnish Spot',
    description='One place rubbed into a mirror.',
    medium='Burnished leaf',
    motion='Polish',
    palette='Mirror gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (237, 29, 30), (18, 226, 225), (232, 230, 177), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 40, 472, 472), outline=ink, width=20)
    draw.rectangle((80, 80, 432, 432), fill=accent)
    
    return canvas.convert("RGBA")
