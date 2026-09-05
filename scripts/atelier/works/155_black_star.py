"""Black zellige. Independent salon work 155."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=155,
    slug='black-star',
    title='Black Star',
    description='A star that swallowed the room.',
    medium='Black zellige',
    motion='Absorb',
    palette='Night tile',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (42, 238, 199), (213, 17, 56), (46, 102, 107), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((60, 60, 452, 452), fill=mid)
    draw.regular_polygon((256 + ox, 256 + oy, int(90 * scale)), 8, fill=accent, outline=ink)
    
    return canvas.convert("RGBA")
