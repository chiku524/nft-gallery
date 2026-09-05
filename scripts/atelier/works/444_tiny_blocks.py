"""Mosaique. Independent salon work 444."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=444,
    slug='tiny-blocks',
    title='Tiny Blocks',
    description='A floor for a smaller building.',
    medium='Mosaique',
    motion='Scatter',
    palette='Toy wood',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (176, 233, 56), (79, 22, 199), (103, 80, 236), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, y in enumerate(range(40, 480, int(28 * scale))):
        draw.rectangle((30 + (i % 3) * 8, y, 482, y + 16), fill=ink if i % 2 == 0 else accent)
        draw.line((30, y + 16, 482, y + 16), fill=mid, width=2)
    
    return canvas.convert("RGBA")
