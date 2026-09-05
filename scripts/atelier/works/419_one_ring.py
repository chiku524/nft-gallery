"""Single ring. Independent salon work 419."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=419,
    slug='one-ring',
    title='One Ring',
    description='The rest of the shirt is implied.',
    medium='Single ring',
    motion='Turn',
    palette='Lone iron',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (17, 63, 131), (238, 192, 124), (166, 88, 88), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((80, 80, 432, 432), outline=ink, width=16)
    draw.ellipse((160, 160, 352, 352), outline=accent, width=10)
    
    return canvas.convert("RGBA")
