"""Basket parquet. Independent salon work 174."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=174,
    slug='basket-oak',
    title='Basket Oak',
    description='Squares pretending they are cloth.',
    medium='Basket parquet',
    motion='Weave',
    palette='Blond oak',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (172, 37, 236), (83, 218, 19), (75, 78, 133), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((48, 48, 464, 464), outline=ink, width=10)
    for i in range(6):
        x = 80 + i * 60
        draw.polygon([(x, 140), (x + 40, 200), (x + 40, 360), (x, 300)], fill=accent if i == frame % 6 else ink)
    
    return canvas.convert("RGBA")
