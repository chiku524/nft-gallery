"""Colored blind. Independent salon work 337."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=337,
    slug='colored-slat',
    title='Colored Slat',
    description='A motel that is only its window.',
    medium='Colored blind',
    motion='Cycle',
    palette='Motel tint',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (75, 177, 156), (180, 78, 99), (21, 36, 24), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 200, 472, 280), fill=ink)
    draw.rectangle((40, 200, 472, 220), fill=accent)
    
    return canvas.convert("RGBA")
