"""Pink aggregate. Independent salon work 147."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=147,
    slug='pink-agg',
    title='Pink Agg',
    description='Candy that pretends it is stone.',
    medium='Pink aggregate',
    motion='Scatter',
    palette='Salon pink',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (135, 161, 145), (12, 12, 14), (108, 174, 134), (73, 86, 79)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((80, 80, 432, 432), fill=mid)
    for i in range(20):
        draw.ellipse((100 + i * 12, 120 + (i * 17) % 200, 130 + i * 12, 150 + (i * 17) % 200), fill=ink)
    
    return canvas.convert("RGBA")
