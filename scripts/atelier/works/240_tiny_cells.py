"""Micro cloisonné. Independent salon work 240."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=240,
    slug='tiny-cells',
    title='Tiny Cells',
    description='Too small to be a story, still a city.',
    medium='Micro cloisonné',
    motion='Glint',
    palette='Bead enamel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (236, 208, 243), (19, 47, 12), (148, 29, 214), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((70, 70, 442, 442), outline=ink, width=8)
    for k in range(8):
        ang = k * math.tau / 8 + t * 0.1
        x, y = 256 + 140 * math.cos(ang), 256 + 140 * math.sin(ang)
        draw.line((256, 256, x, y), fill=ink, width=5)
        draw.ellipse((x - 24, y - 24, x + 24, y + 24), fill=accent)
    
    return canvas.convert("RGBA")
