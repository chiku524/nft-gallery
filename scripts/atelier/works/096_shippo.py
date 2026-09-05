"""Shippo tsunagi. Independent salon work 96."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=96,
    slug='shippo',
    title='Shippo',
    description='Circles that refuse to close.',
    medium='Shippo tsunagi',
    motion='Link',
    palette='Seven jewels',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (39, 64, 85), (216, 191, 170), (173, 125, 223), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(10):
        for j in range(10):
            cx, cy = 50 + i * 44, 50 + j * 44
            draw.arc((cx - 20, cy - 20, cx + 20, cy + 20), 0, 270, fill=ink, width=2)
    
    return canvas.convert("RGBA")
