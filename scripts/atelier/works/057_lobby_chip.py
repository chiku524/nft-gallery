"""Terrazzo chip. Independent salon work 57."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=57,
    slug='lobby-chip',
    title='Lobby Chip',
    description='A floor pouring itself into a wall.',
    medium='Terrazzo chip',
    motion='Settle',
    palette='Lobby mint',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (87, 174, 225), (168, 81, 30), (133, 55, 221), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    rng = np.random.default_rng(21 + int(scale * 10))
    for n in range(int(90 * scale)):
        x, y = int(rng.integers(10, 500)), int(rng.integers(10, 500))
        w, h = int(rng.integers(6, 28)), int(rng.integers(4, 18))
        color = accent if n % 5 == frame % 5 else ink
        draw.polygon([(x, y), (x + w, y + 2), (x + w - 3, y + h), (x - 2, y + h - 1)], fill=color)
    
    return canvas.convert("RGBA")
