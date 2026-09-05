"""Broken ogham. Independent salon work 287."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=287,
    slug='broken-pillar',
    title='Broken Pillar',
    description='The sentence failed mid-word.',
    medium='Broken ogham',
    motion='Gap',
    palette='Ruin score',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (164, 239, 17), (91, 16, 238), (119, 104, 53), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for x in (160, 256, 352):
        draw.line((x, 50, x, 460), fill=ink, width=5)
        for i in range(8):
            y = 70 + i * 48
            draw.line((x - 30, y, x + 30, y - 12), fill=accent, width=3)
    
    return canvas.convert("RGBA")
