"""Packing corrugate. Independent salon work 190."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=190,
    slug='packing-void',
    title='Packing Void',
    description='Protection with nothing to protect.',
    medium='Packing corrugate',
    motion='Cushion',
    palette='Void kraft',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (70, 42, 119), (185, 213, 136), (213, 20, 216), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(8):
        x = 40 + i * 56
        draw.arc((x, 80, x + 56, 432), 270, 90, fill=ink if i % 2 else accent, width=8)
    
    return canvas.convert("RGBA")
