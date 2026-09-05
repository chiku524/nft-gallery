"""Paired ogham. Independent salon work 377."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=377,
    slug='two-edges',
    title='Two Edges',
    description='Two pillars conferring.',
    medium='Paired ogham',
    motion='Face',
    palette='Twin stone',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (201, 153, 109), (54, 102, 146), (230, 147, 90), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
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
