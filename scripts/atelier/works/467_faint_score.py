"""Faint ogham. Independent salon work 467."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=467,
    slug='faint-score',
    title='Faint Score',
    description='Almost gone. Still a law.',
    medium='Faint ogham',
    motion='Whisper',
    palette='Weather stone',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (227, 117, 134), (28, 138, 121), (204, 70, 171), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((80, 400, 430, 90), fill=ink, width=7)
    for i in range(9):
        x = 100 + i * 36
        y = 380 - i * 32
        draw.line((x, y, x + 20, y - 28), fill=accent, width=3)
    
    return canvas.convert("RGBA")
