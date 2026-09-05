"""Single contour. Independent salon work 488."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=488,
    slug='lone-contour',
    title='Lone Contour',
    description='One height. No neighbors.',
    medium='Single contour',
    motion='Hold',
    palette='Lone brown',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (24, 143, 153), (231, 112, 102), (78, 46, 228), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(6):
        r = 50 + i * 30
        draw.ellipse((256 - r, 256 - r, 256 + r, 256 + r), outline=accent if i == frame % 6 else ink, width=3)
    
    return canvas.convert("RGBA")
