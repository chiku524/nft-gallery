"""Chevron parquet. Independent salon work 54."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=54,
    slug='oak-chevron',
    title='Oak Chevron',
    description='A hallway with nowhere to walk.',
    medium='Chevron parquet',
    motion='March',
    palette='Floor honey',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (41, 26, 204), (214, 229, 51), (46, 208, 207), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    w, h = int(70 * scale), int(18 * scale)
    for row in range(16):
        for col in range(10):
            x = 20 + col * (w + 4) + (row % 2) * w // 2
            y = 20 + row * (h + 6)
            tilt = 18 if (row + col) % 2 == 0 else -18
            draw.polygon([(x, y), (x + w, y + tilt), (x + w, y + h + tilt), (x, y + h)], fill=ink if (row + col + frame) % 4 else accent)
    
    return canvas.convert("RGBA")
