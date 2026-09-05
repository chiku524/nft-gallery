"""Sine metal. Independent salon work 160."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=160,
    slug='sine-sheet',
    title='Sine Sheet',
    description='A sheet that refused to stay flat.',
    medium='Sine metal',
    motion='Wave',
    palette='Mill silver',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (41, 119, 61), (214, 136, 194), (207, 240, 39), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((80, 80, 432, 432), fill=mid)
    for x in range(90, 420, 14):
        draw.line((x, 90, x, 420), fill=ink, width=3)
    
    return canvas.convert("RGBA")
