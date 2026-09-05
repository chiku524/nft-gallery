"""Gold bead. Independent salon work 282."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=282,
    slug='gold-bead',
    title='Gold Bead',
    description='Trade that became jewelry.',
    medium='Gold bead',
    motion='Flash',
    palette='Gilt glass',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (124, 28, 114), (131, 227, 141), (180, 141, 205), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(9):
        x = 256 + int(8 * math.sin(t + i))
        draw.ellipse((x - 12, 30 + i * 50, x + 12, 54 + i * 50), fill=accent if i % 2 else ink)
    
    return canvas.convert("RGBA")
