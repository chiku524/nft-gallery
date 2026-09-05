"""Double loop. Independent salon work 159."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=159,
    slug='double-loop',
    title='Double Loop',
    description='Two decisions in one pad.',
    medium='Double loop',
    motion='Braid',
    palette='Twin ink',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (19, 141, 174), (236, 114, 81), (184, 49, 47), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((90, 90, 300, 360), outline=ink, width=3)
    draw.ellipse((220, 140, 430, 400), outline=accent, width=3)
    
    return canvas.convert("RGBA")
