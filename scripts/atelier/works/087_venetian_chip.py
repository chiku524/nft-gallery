"""Venetian terrazzo. Independent salon work 87."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=87,
    slug='venetian-chip',
    title='Venetian Chip',
    description='Marble, reduced to confetti and then promoted.',
    medium='Venetian terrazzo',
    motion='Gleam',
    palette='Palace chip',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (211, 115, 143), (44, 140, 112), (49, 231, 210), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((40, 40, 472, 40), fill=accent, width=8)
    draw.line((40, 40, 40, 472), fill=accent, width=8)
    rng = np.random.default_rng(8)
    for n in range(50):
        x, y = int(rng.integers(60, 450)), int(rng.integers(60, 450))
        draw.ellipse((x, y, x + 16, y + 10), fill=ink if n % 2 else mid)
    
    return canvas.convert("RGBA")
