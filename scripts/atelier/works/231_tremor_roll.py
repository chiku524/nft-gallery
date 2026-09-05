"""Portable seismograph. Independent salon work 231."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=231,
    slug='tremor-roll',
    title='Tremor Roll',
    description='Packed for a ridge. Unpacked as a loop.',
    medium='Portable seismograph',
    motion='Roll',
    palette='Field khaki',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (25, 159, 171), (230, 96, 84), (227, 215, 75), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for row in range(7):
        pts = []
        base = 70 + row * 58
        for x in range(20, 492):
            y = base + int(16 * scale * math.sin(x * 0.08 + t + row))
            pts.append((x, y))
        draw.line(pts, fill=ink if row % 2 == 0 else accent, width=2)
    
    return canvas.convert("RGBA")
