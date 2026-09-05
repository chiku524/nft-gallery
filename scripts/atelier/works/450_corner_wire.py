"""Cloisonné crop. Independent salon work 450."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=450,
    slug='corner-wire',
    title='Corner Wire',
    description='A fragment of a box.',
    medium='Cloisonné crop',
    motion='Crop',
    palette='Edge jewel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (137, 173, 242), (118, 82, 13), (155, 52, 74), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(6):
        for j in range(6):
            draw.rectangle((40 + i * 76, 40 + j * 76, 100 + i * 76, 100 + j * 76), outline=ink, width=4, fill=accent if (i + j + frame) % 4 == 0 else mid)
    
    return canvas.convert("RGBA")
