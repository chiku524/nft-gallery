"""Single cloison. Independent salon work 300."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=300,
    slug='one-cell',
    title='One Cell',
    description='One room of color.',
    medium='Single cloison',
    motion='Hold',
    palette='Lone enamel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (93, 105, 120), (244, 240, 232), (144, 126, 206), (168, 172, 176)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(6):
        for j in range(6):
            draw.rectangle((40 + i * 76, 40 + j * 76, 100 + i * 76, 100 + j * 76), outline=ink, width=4, fill=accent if (i + j + frame) % 4 == 0 else mid)
    
    return canvas.convert("RGBA")
