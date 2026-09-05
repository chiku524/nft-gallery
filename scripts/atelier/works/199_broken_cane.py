"""Broken cane. Independent salon work 199."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=199,
    slug='broken-cane',
    title='Broken Cane',
    description='The seat failed.',
    medium='Broken cane',
    motion='Gap',
    palette='Repair cane',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (101, 68, 101), (154, 187, 154), (201, 216, 113), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(8):
        draw.arc((40 + i * 10, 80, 472 - i * 10, 432), 200, 340, fill=ink if i % 2 else accent, width=3)
    
    return canvas.convert("RGBA")
