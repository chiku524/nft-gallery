"""Square lissajous. Independent salon work 214."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=214,
    slug='square-wave',
    title='Square Wave',
    description='The sine got honest.',
    medium='Square lissajous',
    motion='Chop',
    palette='Logic green',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (68, 215, 117), (187, 40, 138), (156, 129, 96), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
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
