"""Muqarnas crop. Independent salon work 373."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=373,
    slug='corner-cascade',
    title='Corner Cascade',
    description='A fragment of a heaven.',
    medium='Muqarnas crop',
    motion='Crop',
    palette='Edge vault',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (171, 151, 239), (84, 104, 16), (66, 215, 199), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for row in range(7):
        count = 3 + row
        for col in range(count):
            x = 256 - count * 28 + col * 56
            y = 40 + row * 62
            draw.polygon([(x, y + 50), (x + 24, y), (x + 48, y + 50)], fill=ink if (row + col) % 2 else accent, outline=mid)
    
    return canvas.convert("RGBA")
