"""Gilt ogham. Independent salon work 167."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=167,
    slug='gold-score',
    title='Gold Score',
    description='Cuts filled with sun.',
    medium='Gilt ogham',
    motion='Inlay',
    palette='Gilt stone',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (71, 59, 101), (184, 196, 154), (34, 216, 209), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((80, 400, 430, 90), fill=ink, width=7)
    for i in range(9):
        x = 100 + i * 36
        y = 380 - i * 32
        draw.line((x, y, x + 20, y - 28), fill=accent, width=3)
    
    return canvas.convert("RGBA")
