"""Mini check. Independent salon work 415."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=415,
    slug='mini-check',
    title='Mini Check',
    description='Too small for a clan, still a law.',
    medium='Mini check',
    motion='Tick',
    palette='Shirt pale',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (224, 70, 17), (31, 185, 238), (145, 199, 226), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=mid)
    for i in range(14):
        p = int(i * 36 * scale)
        draw.line((p, 0, 512, 512 - p), fill=ink, width=3)
        draw.line((0, p, 512 - p, 512), fill=accent, width=2)
    
    return canvas.convert("RGBA")
