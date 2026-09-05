"""Broken action. Independent salon work 243."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=243,
    slug='broken-action',
    title='Broken Action',
    description='A key that will not return.',
    medium='Broken action',
    motion='Jam',
    palette='Repair ivory',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (191, 144, 115), (12, 12, 14), (211, 99, 228), (101, 78, 64)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for row in range(12):
        y = 20 + row * 40
        for col in range(16):
            if (row * 3 + col + frame) % 7 == 0:
                draw.rectangle((20 + col * 30, y, 44 + col * 30, y + 16), fill=ink)
    
    return canvas.convert("RGBA")
