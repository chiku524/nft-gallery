"""Gold latent. Independent salon work 249."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=249,
    slug='gold-dust',
    title='Gold Dust',
    description='A crime scene dressed for a lobby.',
    medium='Gold latent',
    motion='Spark',
    palette='Show powder',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (117, 43, 48), (138, 212, 207), (131, 176, 50), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(12):
        a0 = -40 + i * 8
        a1 = 40 + i * 8
        draw.arc((80, 80, 432, 432), a0, a1, fill=ink, width=3)
    
    return canvas.convert("RGBA")
