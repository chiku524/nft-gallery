"""Glass terrazzo. Independent salon work 267."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=267,
    slug='glass-agg',
    title='Glass Agg',
    description='A beach that used to be windows.',
    medium='Glass terrazzo',
    motion='Spark',
    palette='Bottle green',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (135, 184, 23), (120, 71, 232), (57, 170, 133), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(12):
        x = 30 + (i * 41 + frame * 7) % 450
        y = 40 + (i * 73) % 420
        draw.regular_polygon((x, y, 18), 3 + (i % 3), fill=accent if i % 2 else ink)
    
    return canvas.convert("RGBA")
