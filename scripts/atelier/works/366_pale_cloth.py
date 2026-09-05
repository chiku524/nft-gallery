"""Pale sashiko. Independent salon work 366."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=366,
    slug='pale-cloth',
    title='Pale Cloth',
    description='Indigo that almost wasn’t.',
    medium='Pale sashiko',
    motion='Whisper',
    palette='Sky hemp',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (234, 243, 100), (21, 12, 155), (45, 207, 72), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for y in range(40, 480, int(22 * scale)):
        for x in range(40, 480, 28):
            if ((x + y) // 20 + frame) % 3:
                draw.line((x, y, x + 12, y), fill=ink, width=3)
    
    return canvas.convert("RGBA")
