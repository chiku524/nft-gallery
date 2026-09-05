"""Checker plate. Independent salon work 88."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=88,
    slug='checker-steel',
    title='Checker Steel',
    description='Raised, repeating, unfriendly.',
    medium='Checker plate',
    motion='Stamp',
    palette='Mill grey',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (75, 80, 174), (180, 175, 81), (21, 37, 94), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((60, 60, 452, 452), fill=mid)
    for i in range(5):
        for j in range(5):
            draw.regular_polygon((120 + i * 70, 120 + j * 70, 22), 4, rotation=45 + t * 4, fill=ink)
    
    return canvas.convert("RGBA")
