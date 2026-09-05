"""Scale fan. Independent salon work 353."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=353,
    slug='scale-fan',
    title='Scale Fan',
    description='One gesture, many lids.',
    medium='Scale fan',
    motion='Open',
    palette='Opera red',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (44, 218, 40), (211, 37, 215), (59, 128, 135), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    step = int(28 * scale)
    for row, y in enumerate(range(20, 520, step)):
        shift = (row % 2) * step // 2 + int(6 * math.sin(t + row))
        for x in range(-20 + shift, 540, step):
            draw.chord((x, y, x + step + 8, y + step + 4), 200, 340, fill=ink if row % 3 else accent, outline=mid)
    
    return canvas.convert("RGBA")
