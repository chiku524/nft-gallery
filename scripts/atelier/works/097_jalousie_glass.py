"""Jalousie. Independent salon work 97."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=97,
    slug='jalousie-glass',
    title='Jalousie Glass',
    description='A climate drawn as slats.',
    medium='Jalousie',
    motion='Crank',
    palette='Miami glass',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (100, 170, 130), (12, 12, 14), (42, 216, 168), (56, 91, 72)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, x in enumerate(range(30, 490, 28)):
        draw.rectangle((x, 40, x + 16, 472), fill=ink if i % 2 else mid)
    
    return canvas.convert("RGBA")
