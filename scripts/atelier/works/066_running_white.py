"""Sashiko. Independent salon work 66."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=66,
    slug='running-white',
    title='Running White',
    description='A repair that became a law.',
    medium='Sashiko',
    motion='Run',
    palette='Indigo white',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (188, 71, 159), (67, 184, 96), (136, 123, 84), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for y in range(40, 480, int(22 * scale)):
        for x in range(40, 480, 28):
            if ((x + y) // 20 + frame) % 3:
                draw.line((x, y, x + 12, y), fill=ink, width=3)
    
    return canvas.convert("RGBA")
