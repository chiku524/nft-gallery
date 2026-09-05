"""Andalusian tile. Independent salon work 125."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=125,
    slug='andusi',
    title='Andusi',
    description='A memory of a courtyard.',
    medium='Andalusian tile',
    motion='Repeat',
    palette='Cordoba glaze',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (21, 126, 28), (234, 129, 227), (70, 168, 230), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(12):
        r = 20 + i * 18
        draw.regular_polygon((256, 256, r), 8, rotation=i * 8 + t * 4, outline=ink)
    
    return canvas.convert("RGBA")
