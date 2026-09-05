"""Paired cane. Independent salon work 469."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=469,
    slug='two-hex',
    title='Two Hex',
    description='Two holes conferring.',
    medium='Paired cane',
    motion='Meet',
    palette='Twin cane',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (110, 17, 164), (145, 238, 91), (52, 162, 238), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((180 + ox, 180 + oy, 332, 332), outline=ink, width=10)
    
    return canvas.convert("RGBA")
