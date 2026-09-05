"""Cell enamel. Independent salon work 90."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=90,
    slug='enamel-well',
    title='Enamel Well',
    description='A well of glass in a metal room.',
    medium='Cell enamel',
    motion='Well',
    palette='Jewel night',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (159, 88, 94), (244, 240, 232), (31, 139, 131), (201, 164, 163)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((70, 70, 442, 442), outline=ink, width=8)
    for k in range(8):
        ang = k * math.tau / 8 + t * 0.1
        x, y = 256 + 140 * math.cos(ang), 256 + 140 * math.sin(ang)
        draw.line((256, 256, x, y), fill=ink, width=5)
        draw.ellipse((x - 24, y - 24, x + 24, y + 24), fill=accent)
    
    return canvas.convert("RGBA")
