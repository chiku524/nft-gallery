"""Marquetry band. Independent salon work 234."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=234,
    slug='inlay-band',
    title='Inlay Band',
    description='A border that thinks it is a river.',
    medium='Marquetry band',
    motion='Trace',
    palette='Satinwood',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (159, 26, 35), (96, 229, 220), (43, 43, 218), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    s = int(36 * scale)
    for y in range(16, 500, s):
        for x in range(16, 500, s):
            draw.rectangle((x, y, x + s - 4, y + s - 4), fill=ink if (x // s + y // s) % 2 else mid, outline=accent)
    
    return canvas.convert("RGBA")
