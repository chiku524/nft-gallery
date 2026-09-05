"""Runway crop. Independent salon work 408."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=408,
    slug='crop-tarmac',
    title='Crop Tarmac',
    description='A fragment of an approach.',
    medium='Runway crop',
    motion='Crop',
    palette='Edge yellow',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (61, 227, 139), (194, 28, 116), (93, 169, 45), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(8):
        draw.rectangle((80 + i * 12, 80, 88 + i * 12, 200), fill=ink)
    draw.rectangle((80, 360, 432, 400), fill=accent)
    
    return canvas.convert("RGBA")
