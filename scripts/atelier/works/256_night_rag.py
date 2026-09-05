"""Night paper. Independent salon work 256."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=256,
    slug='night-rag',
    title='Night Rag',
    description='Pulp after the mill.',
    medium='Night paper',
    motion='Dim',
    palette='Void rag',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (150, 124, 74), (244, 240, 232), (133, 225, 75), (197, 182, 153)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for x in range(40, 480, 18):
        draw.line((x, 40, x, 472), fill=ink, width=1)
    for x in range(40, 480, 72):
        draw.line((x, 40, x, 472), fill=accent, width=3)
    
    return canvas.convert("RGBA")
