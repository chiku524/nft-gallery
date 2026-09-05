"""Night runway. Independent salon work 258."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=258,
    slug='night-tarmac',
    title='Night Tarmac',
    description='The paint after the flights.',
    medium='Night runway',
    motion='Glow',
    palette='Void tarmac',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (172, 238, 224), (83, 17, 31), (72, 20, 142), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(8):
        draw.rectangle((80 + i * 12, 80, 88 + i * 12, 200), fill=ink)
    draw.rectangle((80, 360, 432, 400), fill=accent)
    
    return canvas.convert("RGBA")
