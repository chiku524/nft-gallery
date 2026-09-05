"""Smoked drum. Independent salon work 141."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=141,
    slug='aftershock',
    title='Aftershock',
    description='The second wave is smaller and somehow louder.',
    medium='Smoked drum',
    motion='Jolt',
    palette='Char lamp',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (122, 137, 118), (244, 240, 232), (217, 75, 36), (183, 188, 175)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
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
