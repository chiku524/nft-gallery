"""Corrugated iron. Independent salon work 100."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=100,
    slug='roof-iron',
    title='Roof Iron',
    description='A shed elevated.',
    medium='Corrugated iron',
    motion='Weather',
    palette='Shed rust',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (49, 114, 90), (206, 141, 165), (224, 151, 83), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts_a, pts_b = [], []
    for y in range(0, 512, 4):
        wave = int(16 * scale * math.sin(y * 0.08 + t))
        pts_a.append((180 + wave, y))
        pts_b.append((320 + wave, y))
    draw.line(pts_a, fill=ink, width=10)
    draw.line(pts_b, fill=accent, width=10)
    
    return canvas.convert("RGBA")
