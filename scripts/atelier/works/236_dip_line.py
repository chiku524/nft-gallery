"""Dip dye. Independent salon work 236."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=236,
    slug='dip-line',
    title='Dip Line',
    description='A tide on cloth.',
    medium='Dip dye',
    motion='Lift',
    palette='Horizon indigo',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (85, 48, 204), (170, 207, 51), (78, 86, 239), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(16):
        y = 20 + i * int(30 * scale) + int(10 * math.sin(t + i))
        draw.arc((40, y, 472, y + 80), 0, 180, fill=ink, width=5)
    
    return canvas.convert("RGBA")
