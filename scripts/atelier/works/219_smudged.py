"""Smudged print. Independent salon work 219."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=219,
    slug='smudged',
    title='Smudged',
    description='The identity failed on purpose.',
    medium='Smudged print',
    motion='Smear',
    palette='Bad lift',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (201, 194, 92), (54, 61, 163), (76, 32, 208), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for ring in range(10, int(180 * scale), 8):
        draw.ellipse((256 - ring + ox, 256 - ring + oy, 256 + ring + ox, 256 + ring + oy), outline=ink, width=2)
    
    return canvas.convert("RGBA")
