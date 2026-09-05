"""Roulette ground. Independent salon work 140."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=140,
    slug='roulette',
    title='Roulette',
    description='A wheel that makes dark.',
    medium='Roulette ground',
    motion='Roll',
    palette='Tooth grey',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (16, 212, 76), (239, 43, 179), (177, 198, 200), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    for i in range(40):
        x = 20 + i * 12
        draw.line((x, 20, x + 8, 492), fill=mid, width=1)
    
    return canvas.convert("RGBA")
