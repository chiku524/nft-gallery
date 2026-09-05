"""Seigaiha. Independent salon work 156."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=156,
    slug='seigaiha',
    title='Seigaiha',
    description='Waves that are only stitches.',
    medium='Seigaiha',
    motion='Wave',
    palette='Wave indigo',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (125, 222, 131), (12, 12, 14), (48, 35, 214), (68, 117, 72)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for row in range(9):
        y = 50 + row * 48
        draw.line((40, y, 472, y), fill=mid, width=2)
        for x in range(50, 460, 24):
            draw.line((x, y - 6, x, y + 6), fill=ink, width=3)
    
    return canvas.convert("RGBA")
