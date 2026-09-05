"""Micro terrazzo. Independent salon work 387."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=387,
    slug='tiny-agg',
    title='Tiny Agg',
    description='A floor for a dollhouse atrium.',
    medium='Micro terrazzo',
    motion='Speck',
    palette='Dust marble',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (217, 102, 165), (38, 153, 90), (67, 211, 94), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((40, 40, 472, 40), fill=accent, width=8)
    draw.line((40, 40, 40, 472), fill=accent, width=8)
    rng = np.random.default_rng(8)
    for n in range(50):
        x, y = int(rng.integers(60, 450)), int(rng.integers(60, 450))
        draw.ellipse((x, y, x + 16, y + 10), fill=ink if n % 2 else mid)
    
    return canvas.convert("RGBA")
