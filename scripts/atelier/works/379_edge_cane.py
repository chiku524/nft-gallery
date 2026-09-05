"""Cane crop. Independent salon work 379."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=379,
    slug='edge-cane',
    title='Edge Cane',
    description='A fragment of a chair.',
    medium='Cane crop',
    motion='Crop',
    palette='Edge tan',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (56, 151, 121), (244, 240, 232), (48, 98, 168), (150, 195, 176)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    s = int(36 * scale)
    for y in range(20, 500, s):
        for x in range(20, 500, s):
            draw.ellipse((x, y, x + s, y + s), outline=ink, width=3)
    
    return canvas.convert("RGBA")
