"""Crash bead. Independent salon work 372."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=372,
    slug='color-crash',
    title='Color Crash',
    description='The palette refused manners.',
    medium='Crash bead',
    motion='Clash',
    palette='Fair bead',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (247, 103, 200), (8, 152, 55), (210, 140, 93), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    colors = [ink, accent, mid, bg]
    for row in range(16):
        for col in range(16):
            x = 24 + col * 30 + (row % 2) * 15
            y = 24 + row * 30
            draw.ellipse((x, y, x + 16, y + 16), fill=colors[(row + col + frame) % 4], outline=ink)
    
    return canvas.convert("RGBA")
