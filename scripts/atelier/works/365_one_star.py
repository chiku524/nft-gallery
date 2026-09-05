"""Single zellige. Independent salon work 365."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=365,
    slug='one-star',
    title='One Star',
    description='The rest of the wall is implied.',
    medium='Single zellige',
    motion='Seat',
    palette='Lone star',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (189, 145, 109), (12, 12, 14), (196, 86, 38), (100, 78, 61)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(8):
        for j in range(8):
            cx, cy = 40 + i * 60, 40 + j * 60
            pts = [(cx + 26 * math.cos(k * math.tau / 8 + spin), cy + 26 * math.sin(k * math.tau / 8 + spin)) for k in range(8)]
            draw.polygon([(int(x), int(y)) for x, y in pts], fill=accent if (i + j + frame) % 3 == 0 else ink)
    
    return canvas.convert("RGBA")
