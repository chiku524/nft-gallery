"""Gilt muqarnas. Independent salon work 343."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=343,
    slug='gold-leaf-vault',
    title='Gold Leaf Vault',
    description='Light as structure.',
    medium='Gilt muqarnas',
    motion='Burnish',
    palette='Leaf vault',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (14, 180, 21), (241, 75, 234), (71, 188, 44), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(5):
        for j in range(i + 1):
            x = 256 - i * 30 + j * 60
            y = 80 + i * 70
            draw.regular_polygon((x, y, 24), 3, fill=accent if (i + j + frame) % 3 == 0 else ink)
    
    return canvas.convert("RGBA")
