"""Loose cane. Independent salon work 349."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=349,
    slug='loose-web',
    title='Loose Web',
    description='The seat gave.',
    medium='Loose cane',
    motion='Sag',
    palette='Summer cane',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (109, 138, 181), (12, 12, 14), (107, 128, 103), (60, 75, 97)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(8):
        draw.arc((40 + i * 10, 80, 472 - i * 10, 432), 200, 340, fill=ink if i % 2 else accent, width=3)
    
    return canvas.convert("RGBA")
