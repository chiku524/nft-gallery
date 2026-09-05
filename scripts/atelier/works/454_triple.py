"""Three-tone figure. Independent salon work 454."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=454,
    slug='triple',
    title='Triple',
    description='A third voice enters and ruins the bow.',
    medium='Three-tone figure',
    motion='Braid',
    palette='Triple gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (212, 56, 142), (43, 199, 113), (147, 97, 191), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
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
