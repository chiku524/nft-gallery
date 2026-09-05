"""Piano roll. Independent salon work 93."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=93,
    slug='player-roll',
    title='Player Roll',
    description='Holes that used to be notes.',
    medium='Piano roll',
    motion='Advance',
    palette='Perforated cream',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (186, 69, 126), (69, 186, 129), (223, 159, 92), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for row in range(12):
        y = 20 + row * 40
        for col in range(16):
            if (row * 3 + col + frame) % 7 == 0:
                draw.rectangle((20 + col * 30, y, 44 + col * 30, y + 16), fill=ink)
    
    return canvas.convert("RGBA")
