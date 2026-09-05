"""Night muqarnas. Independent salon work 193."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=193,
    slug='night-vault',
    title='Night Vault',
    description='The ceiling after the lamps.',
    medium='Night muqarnas',
    motion='Dim',
    palette='Moon vault',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (210, 179, 128), (45, 76, 127), (179, 228, 52), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(5):
        for j in range(i + 1):
            x = 256 - i * 30 + j * 60
            y = 80 + i * 70
            draw.regular_polygon((x, y, 24), 3, fill=accent if (i + j + frame) % 3 == 0 else ink)
    
    return canvas.convert("RGBA")
