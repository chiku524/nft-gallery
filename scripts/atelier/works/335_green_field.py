"""Green zellige. Independent salon work 335."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=335,
    slug='green-field',
    title='Green Field',
    description='A garden with no plants.',
    medium='Green zellige',
    motion='Field',
    palette='Garden tile',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (194, 151, 226), (61, 104, 29), (72, 91, 127), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for k in range(6):
        ang = k * math.tau / 6
        draw.regular_polygon((256 + 120 * math.cos(ang), 256 + 120 * math.sin(ang), 40), 8, fill=ink if k % 2 else accent)
    
    return canvas.convert("RGBA")
