"""Black tread. Independent salon work 238."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=238,
    slug='black-plate',
    title='Black Plate',
    description='A warning that learned to whisper.',
    medium='Black tread',
    motion='Absorb',
    palette='Night steel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (230, 186, 226), (25, 69, 29), (107, 65, 188), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((60, 60, 452, 452), fill=mid)
    for i in range(5):
        for j in range(5):
            draw.regular_polygon((120 + i * 70, 120 + j * 70, 22), 4, rotation=45 + t * 4, fill=ink)
    
    return canvas.convert("RGBA")
