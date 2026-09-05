"""Vat void. Independent salon work 356."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=356,
    slug='indigo-void',
    title='Indigo Void',
    description='The cloth went in and almost did not return.',
    medium='Vat void',
    motion='Sink',
    palette='Deep vat',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (38, 233, 80), (217, 22, 175), (184, 129, 114), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    step = int(36 * scale)
    for y in range(30, 490, step):
        for x in range(30 + (y // step % 2) * step // 2, 490, step):
            r = int(8 + 5 * math.sin(t + x * 0.02 + y * 0.02))
            draw.ellipse((x - r, y - r, x + r, y + r), fill=ink)
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=bg)
    
    return canvas.convert("RGBA")
