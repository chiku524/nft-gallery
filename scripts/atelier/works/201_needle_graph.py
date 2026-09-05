"""Galvanometer. Independent salon work 201."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=201,
    slug='needle-graph',
    title='Needle Graph',
    description='A coil arguing with a strip of paper.',
    medium='Galvanometer',
    motion='Sweep',
    palette='Brass pale',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (98, 106, 125), (244, 240, 232), (130, 60, 145), (171, 173, 178)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts = []
    for x in range(24, 488):
        y = 256 + oy + int((70 * scale) * math.sin(x * 0.055 + t) + (28 * scale) * math.sin(x * 0.17 + t * 2))
        pts.append((x + ox // 4, y))
    draw.line(pts, fill=ink, width=max(2, int(3 * scale)))
    
    return canvas.convert("RGBA")
