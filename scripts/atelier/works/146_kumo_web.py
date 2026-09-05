"""Kumo shibori. Independent salon work 146."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=146,
    slug='kumo-web',
    title='Kumo Web',
    description='Tied into a sky.',
    medium='Kumo shibori',
    motion='Pull',
    palette='Spider indigo',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (239, 37, 241), (16, 218, 14), (28, 105, 55), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(7):
        r = int((40 + i * 28) * scale)
        draw.ellipse((256 - r + ox, 256 - r + oy, 256 + r + ox, 256 + r + oy), outline=ink, width=4)
    
    return canvas.convert("RGBA")
