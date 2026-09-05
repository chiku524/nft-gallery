"""Over-inked. Independent salon work 399."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=399,
    slug='over-inked',
    title='Over Inked',
    description='Too much identity.',
    medium='Over-inked',
    motion='Flood',
    palette='Heavy pad',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (29, 203, 114), (226, 52, 141), (207, 57, 26), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(12):
        a0 = -40 + i * 8
        a1 = 40 + i * 8
        draw.arc((80, 80, 432, 432), a0, a1, fill=ink, width=3)
    
    return canvas.convert("RGBA")
