"""Threshold bars. Independent salon work 108."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=108,
    slug='threshold',
    title='Threshold',
    description='The bars that mean here.',
    medium='Threshold bars',
    motion='Hold',
    palette='Piano tarmac',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (48, 16, 54), (207, 239, 201), (55, 25, 201), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(8):
        draw.rectangle((80 + i * 12, 80, 88 + i * 12, 200), fill=ink)
    draw.rectangle((80, 360, 432, 400), fill=accent)
    
    return canvas.convert("RGBA")
