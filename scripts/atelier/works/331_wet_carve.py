"""Wet sgraffito. Independent salon work 331."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=331,
    slug='wet-carve',
    title='Wet Carve',
    description='Carved before it could dry.',
    medium='Wet sgraffito',
    motion='Slip',
    palette='Wet terra',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (177, 81, 27), (78, 174, 228), (101, 115, 125), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.polygon([(80, 400), (256, 80), (430, 400)], outline=bg, width=8)
    
    return canvas.convert("RGBA")
