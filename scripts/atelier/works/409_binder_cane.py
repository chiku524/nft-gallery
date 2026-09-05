"""Binder cane. Independent salon work 409."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=409,
    slug='binder-cane',
    title='Binder Cane',
    description='The wrap that finishes a seat.',
    medium='Binder cane',
    motion='Wrap',
    palette='Wrap tan',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (195, 84, 161), (60, 171, 94), (79, 83, 40), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(12):
        for j in range(12):
            x, y = 20 + i * 40, 20 + j * 40
            draw.arc((x, y, x + 40, y + 40), 0, 180, fill=ink, width=3)
            draw.arc((x + 20, y + 20, x + 60, y + 60), 180, 360, fill=accent, width=3)
    
    return canvas.convert("RGBA")
