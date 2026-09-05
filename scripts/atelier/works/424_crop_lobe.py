"""Lobe crop. Independent salon work 424."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=424,
    slug='crop-lobe',
    title='Crop Lobe',
    description='One petal of a ratio.',
    medium='Lobe crop',
    motion='Crop',
    palette='Edge amber',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (63, 91, 166), (192, 164, 89), (118, 122, 171), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((96, 96, 416, 416), outline=ink, width=6)
    
    return canvas.convert("RGBA")
