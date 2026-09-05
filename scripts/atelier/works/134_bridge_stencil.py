"""Bridged stencil. Independent salon work 134."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=134,
    slug='bridge-stencil',
    title='Bridge Stencil',
    description='The bridges are the drawing.',
    medium='Bridged stencil',
    motion='Hold',
    palette='Army olive',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (229, 202, 78), (26, 53, 177), (150, 192, 159), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(4):
        draw.regular_polygon((130 + i * 90, 256, 40), 5, rotation=t * 4, fill=ink if i % 2 else accent)
    
    return canvas.convert("RGBA")
