"""Miniature cane. Independent salon work 289."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=289,
    slug='tiny-web',
    title='Tiny Web',
    description='A smaller seat.',
    medium='Miniature cane',
    motion='Tick',
    palette='Pocket cane',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (39, 204, 220), (216, 51, 35), (111, 49, 124), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((80, 80, 432, 432), outline=ink, width=8)
    draw.ellipse((160, 160, 352, 352), outline=accent, width=6)
    
    return canvas.convert("RGBA")
