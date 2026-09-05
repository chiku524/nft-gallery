"""Oscilloscope rose. Independent salon work 94."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=94,
    slug='scope-rose',
    title='Scope Rose',
    description='Not a phosphor hold. A ratio.',
    medium='Oscilloscope rose',
    motion='Bloom',
    palette='CRT gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (125, 165, 40), (130, 90, 215), (85, 43, 36), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
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
