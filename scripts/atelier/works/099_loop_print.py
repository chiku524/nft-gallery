"""Loop print. Independent salon work 99."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=99,
    slug='loop-print',
    title='Loop Print',
    description='A loop that never names anyone.',
    medium='Loop print',
    motion='Enter',
    palette='Pad black',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (129, 193, 95), (12, 12, 14), (136, 214, 141), (70, 102, 54)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(12):
        a0 = -40 + i * 8
        a1 = 40 + i * 8
        draw.arc((80, 80, 432, 432), a0, a1, fill=ink, width=3)
    
    return canvas.convert("RGBA")
