"""District check. Independent salon work 295."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=295,
    slug='district-check',
    title='District Check',
    description='Land drawn as crossings.',
    medium='District check',
    motion='Bound',
    palette='Estate rust',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (53, 165, 89), (202, 90, 166), (125, 240, 51), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 40, 472, 472), fill=ink)
    for n in range(8):
        mgn = 60 + n * 22
        draw.rectangle((mgn, mgn, 512 - mgn, 512 - mgn), outline=accent if n % 2 else bg, width=4)
    
    return canvas.convert("RGBA")
