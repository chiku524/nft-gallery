"""Peyote stitch. Independent salon work 102."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=102,
    slug='peyote',
    title='Peyote',
    description='A stagger that is a law.',
    medium='Peyote stitch',
    motion='Offset',
    palette='Medicine bead',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (158, 69, 144), (244, 240, 232), (228, 35, 170), (201, 154, 188)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for row in range(18):
        for col in range(14):
            x = 40 + col * 30 + (row % 2) * 15
            y = 20 + row * 26
            draw.ellipse((x, y, x + 14, y + 14), fill=ink if (row + col) % 3 else accent)
    
    return canvas.convert("RGBA")
