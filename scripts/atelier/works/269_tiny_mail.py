"""Miniature mail. Independent salon work 269."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=269,
    slug='tiny-mail',
    title='Tiny Mail',
    description='A hauberk for no one.',
    medium='Miniature mail',
    motion='Glint',
    palette='Toy steel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (26, 205, 19), (229, 50, 236), (121, 59, 57), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((80, 80, 432, 432), outline=ink, width=16)
    draw.ellipse((160, 160, 352, 352), outline=accent, width=10)
    
    return canvas.convert("RGBA")
