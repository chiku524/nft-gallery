"""Bead plate. Independent salon work 268."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=268,
    slug='micro-tread',
    title='Micro Tread',
    description='Grip at a smaller scale.',
    medium='Bead plate',
    motion='Grit',
    palette='Bead silver',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (134, 63, 145), (244, 240, 232), (173, 26, 209), (189, 151, 188)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.regular_polygon((256 + ox, 256 + oy, int(120 * scale)), 4, rotation=45, fill=ink)
    draw.regular_polygon((256 + ox, 256 + oy, 40), 4, rotation=45 + t * 10, fill=accent)
    
    return canvas.convert("RGBA")
