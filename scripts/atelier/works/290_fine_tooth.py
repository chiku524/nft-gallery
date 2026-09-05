"""Fine rocker. Independent salon work 290."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=290,
    slug='fine-tooth',
    title='Fine Tooth',
    description='A quieter night.',
    medium='Fine rocker',
    motion='Whisper',
    palette='Silk tooth',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (149, 164, 146), (12, 12, 14), (41, 78, 84), (80, 88, 80)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    for i in range(40):
        x = 20 + i * 12
        draw.line((x, 20, x + 8, 492), fill=mid, width=1)
    
    return canvas.convert("RGBA")
