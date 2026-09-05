"""Broken cloisonné. Independent salon work 210."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=210,
    slug='broken-wire',
    title='Broken Wire',
    description='The fence failed. The color stayed.',
    medium='Broken cloisonné',
    motion='Gap',
    palette='Fracture enamel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (152, 27, 240), (103, 228, 15), (46, 180, 63), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    cells = [(80, 80, 220, 240), (200, 70, 430, 200), (220, 190, 460, 400), (60, 230, 230, 450), (180, 300, 340, 470)]
    for n, box in enumerate(cells):
        draw.rectangle(box, fill=accent if n == frame % 5 else mid, outline=ink, width=5)
    
    return canvas.convert("RGBA")
