"""Loom crop. Independent salon work 402."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=402,
    slug='edge-loom',
    title='Edge Loom',
    description='A fragment of a belt.',
    medium='Loom crop',
    motion='Crop',
    palette='Edge glass',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (102, 181, 84), (153, 74, 171), (75, 219, 94), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for row in range(18):
        for col in range(14):
            x = 40 + col * 30 + (row % 2) * 15
            y = 20 + row * 26
            draw.ellipse((x, y, x + 14, y + 14), fill=ink if (row + col) % 3 else accent)
    
    return canvas.convert("RGBA")
