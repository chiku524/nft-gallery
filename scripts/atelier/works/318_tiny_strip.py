"""Model runway. Independent salon work 318."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=318,
    slug='tiny-strip',
    title='Tiny Strip',
    description='A smaller airport.',
    medium='Model runway',
    motion='Toy',
    palette='Pocket tarmac',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (186, 85, 109), (69, 170, 146), (63, 225, 85), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((60, 80, 200, 200, 80, 340, 240, 430), fill=ink, width=14)
    draw.regular_polygon((240, 430, 16), 4, rotation=45, fill=accent)
    
    return canvas.convert("RGBA")
