"""Mineral paper. Independent salon work 263."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=263,
    slug='asphalt-scale',
    title='Asphalt Scale',
    description='Cheap and glittering.',
    medium='Mineral paper',
    motion='Grit',
    palette='Roof black',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (179, 32, 122), (76, 223, 133), (238, 229, 49), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    cx, cy = 256 + ox, 300 + oy
    for i in range(8):
        r = int((40 + i * 22) * scale)
        draw.arc((cx - r, cy - r, cx + r, cy + r), 200 + 8 * math.sin(t), 340, fill=ink, width=6)
    
    return canvas.convert("RGBA")
