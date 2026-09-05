"""Airstrip plate. Independent salon work 478."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=478,
    slug='runway-plate',
    title='Runway Plate',
    description='A landing that never happens.',
    medium='Airstrip plate',
    motion='Align',
    palette='Tarmac silver',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (146, 72, 54), (109, 183, 201), (44, 127, 223), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((30, 30, 482, 482), outline=ink, width=12)
    draw.regular_polygon((256, 256, 90), 4, rotation=45, fill=accent)
    
    return canvas.convert("RGBA")
