"""High-order figure. Independent salon work 154."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=154,
    slug='tight-ratio',
    title='Tight Ratio',
    description='Too many lobes to count politely.',
    medium='High-order figure',
    motion='Weave',
    palette='Fine gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (121, 33, 14), (134, 222, 241), (28, 138, 152), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts = []
    for k in range(200):
        u = k / 200 * math.tau
        x = 256 + int(140 * math.sin(2 * u + t))
        y = 256 + int(140 * (1 if math.sin(3 * u) > 0 else -1) * abs(math.sin(3 * u)))
        pts.append((x, y))
    draw.line(pts, fill=ink, width=5)
    
    return canvas.convert("RGBA")
