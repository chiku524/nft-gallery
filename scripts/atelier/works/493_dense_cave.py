"""Dense muqarnas. Independent salon work 493."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=493,
    slug='dense-cave',
    title='Dense Cave',
    description='Too many heavens.',
    medium='Dense muqarnas',
    motion='Crowd',
    palette='Packed gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (68, 12, 217), (187, 243, 38), (59, 53, 92), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(5):
        for j in range(i + 1):
            x = 256 - i * 30 + j * 60
            y = 80 + i * 70
            draw.regular_polygon((x, y, 24), 3, fill=accent if (i + j + frame) % 3 == 0 else ink)
    
    return canvas.convert("RGBA")
