"""Capsule tile. Independent salon work 442."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=442,
    slug='capsule-hex',
    title='Capsule Hex',
    description='Medicine as architecture.',
    medium='Capsule tile',
    motion='Dock',
    palette='Clinic white',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (22, 185, 87), (233, 70, 168), (208, 20, 115), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
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
