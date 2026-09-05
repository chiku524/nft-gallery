"""Bead loom. Independent salon work 72."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=72,
    slug='loom-row',
    title='Loom Row',
    description='A belt with no waist.',
    medium='Bead loom',
    motion='String',
    palette='Trade bead',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (38, 54, 22), (217, 201, 233), (159, 42, 171), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    colors = [ink, accent, mid, bg]
    for row in range(16):
        for col in range(16):
            x = 24 + col * 30 + (row % 2) * 15
            y = 24 + row * 30
            draw.ellipse((x, y, x + 16, y + 16), fill=colors[(row + col + frame) % 4], outline=ink)
    
    return canvas.convert("RGBA")
