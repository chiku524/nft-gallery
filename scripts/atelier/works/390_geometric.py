"""Geometric cloisonné. Independent salon work 390."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=390,
    slug='geometric',
    title='Geometric',
    description='No flowers. Only law.',
    medium='Geometric cloisonné',
    motion='Lock',
    palette='Deco enamel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (153, 92, 214), (102, 163, 41), (78, 106, 91), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((70, 70, 442, 442), outline=ink, width=8)
    for k in range(8):
        ang = k * math.tau / 8 + t * 0.1
        x, y = 256 + 140 * math.cos(ang), 256 + 140 * math.sin(ang)
        draw.line((256, 256, x, y), fill=ink, width=5)
        draw.ellipse((x - 24, y - 24, x + 24, y + 24), fill=accent)
    
    return canvas.convert("RGBA")
