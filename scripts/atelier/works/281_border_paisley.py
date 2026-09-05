"""Paisley border. Independent salon work 281."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=281,
    slug='border-paisley',
    title='Border Paisley',
    description='The edge doing all the talking.',
    medium='Paisley border',
    motion='March',
    palette='Edge kashmir',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (145, 40, 195), (110, 215, 60), (20, 61, 30), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(6):
        x = 70 + (i % 3) * 140
        y = 90 + (i // 3) * 180
        draw.pieslice((x, y, x + 120, y + 160), 200, 20, fill=ink if i % 2 else accent)
    
    return canvas.convert("RGBA")
