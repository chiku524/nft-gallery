"""Dense sashiko. Independent salon work 306."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=306,
    slug='dense-run',
    title='Dense Run',
    description='So many repairs the cloth is new.',
    medium='Dense sashiko',
    motion='Fill',
    palette='Work indigo',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (63, 213, 147), (192, 42, 108), (160, 22, 187), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for row in range(9):
        y = 50 + row * 48
        draw.line((40, y, 472, y), fill=mid, width=2)
        for x in range(50, 460, 24):
            draw.line((x, y - 6, x, y + 6), fill=ink, width=3)
    
    return canvas.convert("RGBA")
