"""Gilt terrazzo. Independent salon work 357."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=357,
    slug='gold-chip',
    title='Gold Chip',
    description='Ostentation, ground flat.',
    medium='Gilt terrazzo',
    motion='Flash',
    palette='Gilt lobby',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (240, 226, 82), (15, 29, 173), (153, 46, 154), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    rng = np.random.default_rng(21 + int(scale * 10))
    for n in range(int(90 * scale)):
        x, y = int(rng.integers(10, 500)), int(rng.integers(10, 500))
        w, h = int(rng.integers(6, 28)), int(rng.integers(4, 18))
        color = accent if n % 5 == frame % 5 else ink
        draw.polygon([(x, y), (x + w, y + 2), (x + w - 3, y + h), (x - 2, y + h - 1)], fill=color)
    
    return canvas.convert("RGBA")
