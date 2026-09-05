"""Cellular map. Independent salon work 322."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=322,
    slug='cell-map',
    title='Cell Map',
    description='Addresses for a city that is only corners.',
    medium='Cellular map',
    motion='Index',
    palette='Planner blue',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (78, 108, 126), (244, 240, 232), (25, 144, 54), (161, 174, 179)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 40, 472, 472), outline=ink, width=6)
    r = int(90 * scale)
    draw.regular_polygon((256 + ox, 256 + oy, r), 6, rotation=t * 8, fill=accent, outline=ink)
    
    return canvas.convert("RGBA")
