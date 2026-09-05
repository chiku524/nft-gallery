"""Stamp seismograph. Independent salon work 471."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=471,
    slug='postage-jolt',
    title='Postage Jolt',
    description='The quake, reduced to a denomination.',
    medium='Stamp seismograph',
    motion='Crop',
    palette='Carmine pulp',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (74, 58, 127), (181, 197, 128), (201, 171, 167), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((90, 110, 422, 402), outline=ink, width=8)
    pts = []
    for x in range(110, 402):
        y = 256 + int(40 * math.sin(x * 0.12 + t))
        pts.append((x, y))
    draw.line(pts, fill=accent, width=3)
    
    return canvas.convert("RGBA")
