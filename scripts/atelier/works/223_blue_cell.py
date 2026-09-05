"""Blue muqarnas. Independent salon work 223."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=223,
    slug='blue-cell',
    title='Blue Cell',
    description='A sky hanging downward.',
    medium='Blue muqarnas',
    motion='Well',
    palette='Isfahan blue',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (85, 170, 245), (170, 85, 10), (203, 52, 153), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for row in range(7):
        count = 3 + row
        for col in range(count):
            x = 256 - count * 28 + col * 56
            y = 40 + row * 62
            draw.polygon([(x, y + 50), (x + 24, y), (x + 48, y + 50)], fill=ink if (row + col) % 2 else accent, outline=mid)
    
    return canvas.convert("RGBA")
