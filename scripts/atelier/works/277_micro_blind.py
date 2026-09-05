"""Mini blind. Independent salon work 277."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=277,
    slug='micro-blind',
    title='Micro Blind',
    description='A smaller refusal.',
    medium='Mini blind',
    motion='Tick',
    palette='Desk white',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (116, 235, 207), (139, 20, 48), (200, 204, 42), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((80, 40, 432, 472), outline=ink, width=10)
    for y in range(70, 450, 24):
        draw.rectangle((100, y, 412, y + 10), fill=accent)
    
    return canvas.convert("RGBA")
