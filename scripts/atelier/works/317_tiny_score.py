"""Miniature ogham. Independent salon work 317."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=317,
    slug='tiny-score',
    title='Tiny Score',
    description='A smaller name.',
    medium='Miniature ogham',
    motion='Tick',
    palette='Pocket stone',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (44, 37, 27), (211, 218, 228), (70, 129, 105), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((80, 400, 430, 90), fill=ink, width=7)
    for i in range(9):
        x = 100 + i * 36
        y = 380 - i * 32
        draw.line((x, y, x + 20, y - 28), fill=accent, width=3)
    
    return canvas.convert("RGBA")
