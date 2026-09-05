"""Night corrugate. Independent salon work 280."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=280,
    slug='night-iron',
    title='Night Iron',
    description='The shed after closing.',
    medium='Night corrugate',
    motion='Dim',
    palette='Yard black',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (44, 13, 141), (211, 242, 114), (209, 106, 124), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, y in enumerate(range(0, 512, 16)):
        draw.rectangle((0, y, 512, y + 8), fill=ink if i % 2 else mid)
    
    return canvas.convert("RGBA")
