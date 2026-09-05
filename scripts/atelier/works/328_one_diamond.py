"""Single tread. Independent salon work 328."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=328,
    slug='one-diamond',
    title='One Diamond',
    description='One raised fact.',
    medium='Single tread',
    motion='Seat',
    palette='Lone plate',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (104, 42, 158), (151, 213, 97), (111, 67, 103), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((30, 30, 482, 482), outline=ink, width=12)
    draw.regular_polygon((256, 256, 90), 4, rotation=45, fill=accent)
    
    return canvas.convert("RGBA")
