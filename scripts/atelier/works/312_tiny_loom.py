"""Miniature loom. Independent salon work 312."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=312,
    slug='tiny-loom',
    title='Tiny Loom',
    description='A smaller treaty.',
    medium='Miniature loom',
    motion='Tick',
    palette='Pocket bead',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (39, 197, 41), (216, 58, 214), (29, 125, 88), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(20):
        draw.ellipse((40 + i * 22, 240, 56 + i * 22, 256), fill=ink if i % 2 else accent)
    
    return canvas.convert("RGBA")
