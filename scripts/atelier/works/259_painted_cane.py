"""Painted wicker. Independent salon work 259."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=259,
    slug='painted-cane',
    title='Painted Cane',
    description='A weave that took a color.',
    medium='Painted wicker',
    motion='Coat',
    palette='Porch green',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (167, 160, 188), (88, 95, 67), (49, 187, 197), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(12):
        for j in range(12):
            x, y = 20 + i * 40, 20 + j * 40
            draw.arc((x, y, x + 40, y + 40), 0, 180, fill=ink, width=3)
            draw.arc((x + 20, y + 20, x + 60, y + 60), 180, 360, fill=accent, width=3)
    
    return canvas.convert("RGBA")
