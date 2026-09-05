"""Knoll. Independent salon work 428."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=428,
    slug='tiny-knoll',
    title='Tiny Knoll',
    description='A hill for a smaller country.',
    medium='Knoll',
    motion='Rise',
    palette='Pocket brown',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (112, 120, 202), (12, 12, 14), (68, 160, 117), (62, 66, 108)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(8):
        r = 40 + i * 24
        draw.ellipse((200 - r, 300 - r, 200 + r, 300 + r), outline=ink, width=2)
        draw.line((200 - 8, 300 + r, 200 + 8, 300 + r), fill=accent, width=2)
    
    return canvas.convert("RGBA")
