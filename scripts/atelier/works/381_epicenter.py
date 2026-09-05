"""Iso-seismal. Independent salon work 381."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=381,
    slug='epicenter',
    title='Epicenter',
    description='Rings that mean trouble, drawn as if they were weather.',
    medium='Iso-seismal',
    motion='Bloom',
    palette='Map rose',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (187, 58, 229), (68, 197, 26), (170, 172, 143), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
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
