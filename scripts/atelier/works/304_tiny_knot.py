"""Miniature figure. Independent salon work 304."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=304,
    slug='tiny-knot',
    title='Tiny Knot',
    description='A whole argument, small.',
    medium='Miniature figure',
    motion='Spin',
    palette='Pocket amber',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (168, 196, 92), (87, 59, 163), (37, 85, 74), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
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
