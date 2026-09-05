"""Loose leaf. Independent salon work 495."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=495,
    slug='loose-leaf',
    title='Loose Leaf',
    description='Not yet stuck.',
    medium='Loose leaf',
    motion='Drift',
    palette='Floating gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (25, 148, 73), (230, 107, 182), (86, 95, 60), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 40, 472, 472), outline=ink, width=20)
    draw.rectangle((80, 80, 432, 432), fill=accent)
    
    return canvas.convert("RGBA")
