"""Seismograph ink. Independent salon work 51."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=51,
    slug='jolt-trace',
    title='Jolt Trace',
    description='A needle that writes the floor and will not lift.',
    medium='Seismograph ink',
    motion='Tick',
    palette='Graphite cream',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (188, 39, 53), (67, 216, 202), (133, 41, 41), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts = []
    for x in range(24, 488):
        y = 256 + oy + int((70 * scale) * math.sin(x * 0.055 + t) + (28 * scale) * math.sin(x * 0.17 + t * 2))
        pts.append((x + ox // 4, y))
    draw.line(pts, fill=ink, width=max(2, int(3 * scale)))
    
    return canvas.convert("RGBA")
