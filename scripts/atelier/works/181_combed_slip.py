"""Combed slip. Independent salon work 181."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=181,
    slug='combed-slip',
    title='Combed Slip',
    description='Fingers, replaced by a tool, replaced by a loop.',
    medium='Combed slip',
    motion='Drag',
    palette='Comb clay',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (50, 182, 37), (205, 73, 218), (236, 235, 156), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.polygon([(80, 400), (256, 80), (430, 400)], outline=bg, width=8)
    
    return canvas.convert("RGBA")
