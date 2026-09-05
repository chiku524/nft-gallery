"""Gilt mail. Independent salon work 149."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=149,
    slug='gold-mail',
    title='Gold Mail',
    description='Ceremony that could still cut.',
    medium='Gilt mail',
    motion='Gleam',
    palette='Relic gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (119, 16, 137), (136, 239, 118), (76, 121, 28), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    r = int(70 * scale)
    draw.ellipse((256 - r + ox, 256 - r + oy, 256 + r + ox, 256 + r + oy), outline=ink, width=14)
    draw.ellipse((256 - 12, 256 - 12, 256 + 12, 256 + 12), fill=accent)
    
    return canvas.convert("RGBA")
