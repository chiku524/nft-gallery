"""Single sashiko. Independent salon work 276."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=276,
    slug='one-row',
    title='One Row',
    description='One repair across a night.',
    medium='Single sashiko',
    motion='Sew',
    palette='Lone running',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (112, 138, 126), (244, 240, 232), (74, 207, 34), (178, 189, 179)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(7):
        for j in range(7):
            cx, cy = 70 + i * 60, 70 + j * 60
            for k in range(6):
                ang = k * math.tau / 6
                draw.line((cx, cy, cx + 22 * math.cos(ang), cy + 22 * math.sin(ang)), fill=ink, width=2)
    
    return canvas.convert("RGBA")
