"""Night sashiko. Independent salon work 456."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=456,
    slug='night-mend',
    title='Night Mend',
    description='Mending in the dark.',
    medium='Night sashiko',
    motion='Run',
    palette='Void indigo',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (196, 200, 46), (59, 55, 209), (95, 151, 51), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for row in range(9):
        y = 50 + row * 48
        draw.line((40, y, 472, y), fill=mid, width=2)
        for x in range(50, 460, 24):
            draw.line((x, y - 6, x, y + 6), fill=ink, width=3)
    
    return canvas.convert("RGBA")
