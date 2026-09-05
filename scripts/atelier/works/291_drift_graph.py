"""Tiltmeter. Independent salon work 291."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=291,
    slug='drift-graph',
    title='Drift Graph',
    description='The room is moving. The ink admits it.',
    medium='Tiltmeter',
    motion='Lean',
    palette='Clay slip',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (43, 149, 72), (212, 106, 183), (185, 116, 82), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts = [(20, 480)]
    for x in range(20, 492):
        y = 300 + int((90 * scale) * math.sin(x * 0.04 + t))
        pts.append((x, y))
    pts.append((492, 480))
    draw.polygon(pts, fill=ink)
    draw.polygon([(p[0], p[1] - 8) for p in pts[1:-1]], outline=accent)
    
    return canvas.convert("RGBA")
