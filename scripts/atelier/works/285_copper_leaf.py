"""Copper leaf. Independent salon work 285."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=285,
    slug='copper-leaf',
    title='Copper Leaf',
    description='A cheaper sun.',
    medium='Copper leaf',
    motion='Tarnish',
    palette='Penny leaf',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (18, 217, 246), (237, 38, 9), (208, 217, 41), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(16):
        x, y = 40 + (i * 53) % 420, 40 + (i * 97) % 420
        draw.rectangle((x, y, x + 36, y + 36), fill=ink if i % 2 else accent)
    
    return canvas.convert("RGBA")
