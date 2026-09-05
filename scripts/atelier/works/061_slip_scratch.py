"""Sgraffito. Independent salon work 61."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=61,
    slug='slip-scratch',
    title='Slip Scratch',
    description='Through the pale into the dark.',
    medium='Sgraffito',
    motion='Carve',
    palette='Terracotta slip',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (78, 67, 29), (177, 188, 226), (21, 61, 213), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    for i in range(18):
        x0, y0 = 20 + i * 26, 30
        draw.line((x0, y0, x0 + 80, 490), fill=bg, width=3)
    
    return canvas.convert("RGBA")
