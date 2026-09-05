"""Louver. Independent salon work 307."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=307,
    slug='exterior-louver',
    title='Exterior Louver',
    description='A facade’s eyelashes.',
    medium='Louver',
    motion='Shade',
    palette='Brutal concrete',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (186, 213, 189), (69, 42, 66), (25, 204, 20), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    gap = int(18 + 10 * math.sin(t))
    for y in range(0, 512, 36):
        draw.rectangle((0, y, 512, y + gap), fill=bg)
    
    return canvas.convert("RGBA")
