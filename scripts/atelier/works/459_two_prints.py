"""Paired prints. Independent salon work 459."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=459,
    slug='two-prints',
    title='Two Prints',
    description='A meeting that is only ridges.',
    medium='Paired prints',
    motion='Meet',
    palette='Twin pad',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (125, 136, 39), (244, 240, 232), (33, 177, 121), (184, 188, 135)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((90, 90, 300, 360), outline=ink, width=3)
    draw.ellipse((220, 140, 430, 400), outline=accent, width=3)
    
    return canvas.convert("RGBA")
