"""Partial print. Independent salon work 279."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=279,
    slug='partial',
    title='Partial',
    description='Not enough for a court. Enough for a painting.',
    medium='Partial print',
    motion='Crop',
    palette='Edge pad',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (247, 45, 187), (8, 210, 68), (142, 67, 55), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(14):
        draw.arc((60, 140 + i * 12, 452, 360 + i * 12), 200, 340, fill=ink, width=2)
    
    return canvas.convert("RGBA")
