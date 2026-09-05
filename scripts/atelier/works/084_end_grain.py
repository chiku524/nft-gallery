"""End-grain block. Independent salon work 84."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=84,
    slug='end-grain',
    title='End Grain',
    description='The tree seen the hard way.',
    medium='End-grain block',
    motion='Seat',
    palette='Butcher warm',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (103, 212, 148), (152, 43, 107), (44, 171, 147), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    s = int(36 * scale)
    for y in range(16, 500, s):
        for x in range(16, 500, s):
            draw.rectangle((x, y, x + s - 4, y + s - 4), fill=ink if (x // s + y // s) % 2 else mid, outline=accent)
    
    return canvas.convert("RGBA")
