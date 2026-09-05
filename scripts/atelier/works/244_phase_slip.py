"""Phase portrait. Independent salon work 244."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=244,
    slug='phase-slip',
    title='Phase Slip',
    description='The second channel arrived late.',
    medium='Phase portrait',
    motion='Slip',
    palette='Phase violet',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (145, 153, 201), (110, 102, 54), (29, 29, 86), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts = []
    for k in range(400):
        u = k / 400 * math.tau
        x = 256 + int(180 * math.sin(5 * u + t))
        y = 256 + int(180 * math.sin(4 * u + t * 0.5))
        pts.append((x, y))
    draw.line(pts, fill=accent, width=3)
    
    return canvas.convert("RGBA")
