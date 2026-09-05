"""Cloud cloisonné. Independent salon work 150."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=150,
    slug='cloud-wire',
    title='Cloud Wire',
    description='Weather, soldered.',
    medium='Cloud cloisonné',
    motion='Drift',
    palette='Sky enamel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (234, 65, 120), (21, 190, 135), (181, 141, 209), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(6):
        for j in range(6):
            draw.rectangle((40 + i * 76, 40 + j * 76, 100 + i * 76, 100 + j * 76), outline=ink, width=4, fill=accent if (i + j + frame) % 4 == 0 else mid)
    
    return canvas.convert("RGBA")
