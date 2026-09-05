"""Paisley block. Independent salon work 431."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=431,
    slug='block-paisley',
    title='Block Paisley',
    description='Printed, not woven.',
    medium='Paisley block',
    motion='Stamp',
    palette='Wood dye',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (172, 238, 200), (83, 17, 55), (189, 105, 144), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(6):
        x = 70 + (i % 3) * 140
        y = 90 + (i // 3) * 180
        draw.pieslice((x, y, x + 120, y + 160), 200, 20, fill=ink if i % 2 else accent)
    
    return canvas.convert("RGBA")
