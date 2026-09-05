"""Rice resist. Independent salon work 386."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=386,
    slug='rice-dot',
    title='Rice Dot',
    description='Food used as a dam.',
    medium='Rice resist',
    motion='Speck',
    palette='Grain blue',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (64, 96, 89), (191, 159, 166), (60, 115, 167), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(16):
        y = 20 + i * int(30 * scale) + int(10 * math.sin(t + i))
        draw.arc((40, y, 472, y + 80), 0, 180, fill=ink, width=5)
    
    return canvas.convert("RGBA")
