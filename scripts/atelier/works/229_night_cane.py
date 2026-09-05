"""Night rattan. Independent salon work 229."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=229,
    slug='night-cane',
    title='Night Cane',
    description='The porch after dinner.',
    medium='Night rattan',
    motion='Dim',
    palette='Void tan',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (103, 192, 51), (152, 63, 204), (170, 164, 69), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    s = int(36 * scale)
    for y in range(20, 500, s):
        for x in range(20, 500, s):
            draw.ellipse((x, y, x + s, y + s), outline=ink, width=3)
    
    return canvas.convert("RGBA")
