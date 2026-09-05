"""Broken blind. Independent salon work 247."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=247,
    slug='broken-slat',
    title='Broken Slat',
    description='The view leaks.',
    medium='Broken blind',
    motion='Gap',
    palette='Repair slat',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (53, 49, 218), (202, 206, 37), (137, 157, 79), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, x in enumerate(range(30, 490, 28)):
        draw.rectangle((x, 40, x + 16, 472), fill=ink if i % 2 else mid)
    
    return canvas.convert("RGBA")
