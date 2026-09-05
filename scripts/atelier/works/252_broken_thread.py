"""Broken loom. Independent salon work 252."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=252,
    slug='broken-thread',
    title='Broken Thread',
    description='The belt failed.',
    medium='Broken loom',
    motion='Gap',
    palette='Snap bead',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (86, 36, 102), (169, 219, 153), (239, 116, 87), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for row in range(18):
        for col in range(14):
            x = 40 + col * 30 + (row % 2) * 15
            y = 20 + row * 26
            draw.ellipse((x, y, x + 14, y + 14), fill=ink if (row + col) % 3 else accent)
    
    return canvas.convert("RGBA")
