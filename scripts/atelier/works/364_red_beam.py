"""Red figure. Independent salon work 364."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=364,
    slug='red-beam',
    title='Red Beam',
    description='A warning that learned choreography.',
    medium='Red figure',
    motion='Burn',
    palette='Alert red',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (154, 21, 96), (101, 234, 159), (94, 223, 50), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts = []
    a, b = 3, 2
    for k in range(360):
        u = k / 360 * math.tau
        x = 256 + ox + int(160 * scale * math.sin(a * u + t))
        y = 256 + oy + int(160 * scale * math.sin(b * u))
        pts.append((x, y))
    draw.line(pts, fill=ink, width=4)
    
    return canvas.convert("RGBA")
