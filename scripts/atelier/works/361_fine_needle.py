"""Needle sgraffito. Independent salon work 361."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=361,
    slug='fine-needle',
    title='Fine Needle',
    description='Almost engraving.',
    medium='Needle sgraffito',
    motion='Tick',
    palette='Needle clay',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (197, 195, 68), (58, 60, 187), (218, 54, 45), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    for i in range(18):
        x0, y0 = 20 + i * 26, 30
        draw.line((x0, y0, x0 + 80, 490), fill=bg, width=3)
    
    return canvas.convert("RGBA")
