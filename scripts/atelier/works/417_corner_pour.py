"""Terrazzo crop. Independent salon work 417."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=417,
    slug='corner-pour',
    title='Corner Pour',
    description='Only the accident remains.',
    medium='Terrazzo crop',
    motion='Crop',
    palette='Edge chip',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (211, 143, 211), (44, 112, 44), (66, 218, 220), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(12):
        x = 30 + (i * 41 + frame * 7) % 450
        y = 40 + (i * 73) % 420
        draw.regular_polygon((x, y, 18), 3 + (i % 3), fill=accent if i % 2 else ink)
    
    return canvas.convert("RGBA")
