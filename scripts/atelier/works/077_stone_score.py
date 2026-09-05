"""Ogham. Independent salon work 77."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=77,
    slug='stone-score',
    title='Stone Score',
    description='A language of cuts along an edge.',
    medium='Ogham',
    motion='Score',
    palette='Standing stone',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (212, 48, 153), (43, 207, 102), (153, 167, 73), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((256 + ox, 40, 256 + ox, 472), fill=ink, width=6)
    rng = np.random.default_rng(12)
    for i in range(14):
        y = 50 + i * 30
        side = 1 if i % 2 == 0 else -1
        n = 1 + (i + frame) % 5
        for k in range(n):
            draw.line((256, y + k * 5, 256 + side * 40 * scale, y + k * 5 - 10), fill=ink, width=3)
    
    return canvas.convert("RGBA")
