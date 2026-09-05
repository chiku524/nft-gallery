"""Light leak. Independent salon work 457."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=457,
    slug='leaking-light',
    title='Leaking Light',
    description='The sun wins a little.',
    medium='Light leak',
    motion='Stripe',
    palette='Dawn slat',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (60, 36, 167), (195, 219, 88), (182, 152, 44), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    gap = int(18 + 10 * math.sin(t))
    for y in range(0, 512, 36):
        draw.rectangle((0, y, 512, y + gap), fill=bg)
    
    return canvas.convert("RGBA")
