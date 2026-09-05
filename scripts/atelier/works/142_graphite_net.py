"""Graphene sketch. Independent salon work 142."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=142,
    slug='graphite-net',
    title='Graphite Net',
    description='Six-sided and almost not there.',
    medium='Graphene sketch',
    motion='Drift',
    palette='Pencil silver',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (21, 75, 198), (234, 180, 57), (77, 144, 144), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    s = int(14 * scale)
    for row in range(20):
        for col in range(20):
            cx = col * s * 1.7 + (row % 2) * 12
            cy = row * s * 1.5
            if (row + col + frame) % 5 == 0:
                draw.regular_polygon((cx, cy, s * 0.55), 6, rotation=spin * 40, fill=accent)
            else:
                draw.regular_polygon((cx, cy, s * 0.4), 6, outline=ink)
    
    return canvas.convert("RGBA")
