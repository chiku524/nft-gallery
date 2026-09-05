"""Oscillograph. Independent salon work 441."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=441,
    slug='amp-trace',
    title='Amp Trace',
    description='Voltage pretending it has a landscape.',
    medium='Oscillograph',
    motion='Drive',
    palette='Amber bakelite',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (98, 96, 99), (244, 240, 232), (117, 201, 208), (171, 168, 165)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
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
