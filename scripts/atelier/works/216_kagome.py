"""Kagome. Independent salon work 216."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=216,
    slug='kagome',
    title='Kagome',
    description='A basket that is only holes.',
    medium='Kagome',
    motion='Weave',
    palette='Basket stitch',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (172, 84, 100), (83, 171, 155), (20, 166, 228), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for y in range(40, 480, int(22 * scale)):
        for x in range(40, 480, 28):
            if ((x + y) // 20 + frame) % 3:
                draw.line((x, y, x + 12, y), fill=ink, width=3)
    
    return canvas.convert("RGBA")
