"""Tesuji. Independent salon work 296."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=296,
    slug='tesuji',
    title='Tesuji',
    description='Pleats that dye like a riverbed.',
    medium='Tesuji',
    motion='Pleat',
    palette='Hand indigo',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (95, 81, 120), (244, 240, 232), (82, 162, 198), (169, 160, 176)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(7):
        r = int((40 + i * 28) * scale)
        draw.ellipse((256 - r + ox, 256 - r + oy, 256 + r + ox, 256 + r + oy), outline=ink, width=4)
    
    return canvas.convert("RGBA")
