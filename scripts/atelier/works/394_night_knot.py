"""Night lissajous. Independent salon work 394."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=394,
    slug='night-knot',
    title='Night Knot',
    description='The room is the afterglow.',
    medium='Night lissajous',
    motion='Orbit',
    palette='Void gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (168, 84, 151), (12, 12, 14), (200, 123, 47), (90, 48, 82)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
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
