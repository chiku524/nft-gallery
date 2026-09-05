"""Two-pass stencil. Independent salon work 434."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=434,
    slug='two-color',
    title='Two Color',
    description='The second pass missed and stayed.',
    medium='Two-pass stencil',
    motion='Register',
    palette='Pass spray',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (129, 124, 235), (126, 131, 20), (145, 91, 162), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(4):
        draw.regular_polygon((130 + i * 90, 256, 40), 5, rotation=t * 4, fill=ink if i % 2 else accent)
    
    return canvas.convert("RGBA")
