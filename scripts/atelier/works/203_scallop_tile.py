"""Scallop tile. Independent salon work 203."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=203,
    slug='scallop-tile',
    title='Scallop Tile',
    description='A wall learning to be a shore.',
    medium='Scallop tile',
    motion='Lap',
    palette='Bath cream',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (135, 218, 206), (120, 37, 49), (130, 215, 233), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    step = int(28 * scale)
    for row, y in enumerate(range(20, 520, step)):
        shift = (row % 2) * step // 2 + int(6 * math.sin(t + row))
        for x in range(-20 + shift, 540, step):
            draw.chord((x, y, x + step + 8, y + step + 4), 200, 340, fill=ink if row % 3 else accent, outline=mid)
    
    return canvas.convert("RGBA")
