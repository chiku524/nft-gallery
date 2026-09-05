"""Rattan peel. Independent salon work 139."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=139,
    slug='rattan-peel',
    title='Rattan Peel',
    description='Skin of a vine.',
    medium='Rattan peel',
    motion='Wind',
    palette='Peel tan',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (128, 229, 67), (127, 26, 188), (125, 133, 124), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((80, 80, 432, 432), outline=ink, width=8)
    draw.ellipse((160, 160, 352, 352), outline=accent, width=6)
    
    return canvas.convert("RGBA")
