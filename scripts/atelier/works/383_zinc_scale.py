"""Zinc shingle. Independent salon work 383."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=383,
    slug='zinc-scale',
    title='Zinc Scale',
    description='A shed elevated to a painting.',
    medium='Zinc shingle',
    motion='Weather',
    palette='Industrial pale',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (54, 123, 124), (244, 240, 232), (37, 145, 94), (149, 181, 178)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(9):
        y = 40 + i * 48
        draw.pieslice((80, y, 430, y + 90), 200, 340, fill=ink if i % 2 == 0 else accent, outline=mid)
    
    return canvas.convert("RGBA")
