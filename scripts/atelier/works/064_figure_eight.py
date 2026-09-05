"""Lissajous. Independent salon work 64."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=64,
    slug='figure-eight',
    title='Figure Eight',
    description='Two tones arguing until they draw a knot.',
    medium='Lissajous',
    motion='Knot',
    palette='Scope amber',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (26, 71, 38), (229, 184, 217), (235, 32, 102), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
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
