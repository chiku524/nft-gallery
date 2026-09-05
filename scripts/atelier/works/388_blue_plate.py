"""Painted tread. Independent salon work 388."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=388,
    slug='blue-plate',
    title='Blue Plate',
    description='Shop paint over a threat.',
    medium='Painted tread',
    motion='Coat',
    palette='Machine blue',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (167, 189, 188), (88, 66, 67), (100, 86, 186), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((60, 60, 452, 452), fill=mid)
    for i in range(5):
        for j in range(5):
            draw.regular_polygon((120 + i * 70, 120 + j * 70, 22), 4, rotation=45 + t * 4, fill=ink)
    
    return canvas.convert("RGBA")
