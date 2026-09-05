"""Micro zellige. Independent salon work 305."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=305,
    slug='tiny-cuts',
    title='Tiny Cuts',
    description='A wall for a smaller riad.',
    medium='Micro zellige',
    motion='Glint',
    palette='Chip glaze',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (240, 63, 73), (15, 192, 182), (80, 187, 94), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((60, 60, 452, 452), fill=mid)
    draw.regular_polygon((256 + ox, 256 + oy, int(90 * scale)), 8, fill=accent, outline=ink)
    
    return canvas.convert("RGBA")
