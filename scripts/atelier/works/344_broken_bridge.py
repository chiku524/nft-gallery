"""Broken stencil. Independent salon work 344."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=344,
    slug='broken-bridge',
    title='Broken Bridge',
    description='The letter leaked.',
    medium='Broken stencil',
    motion='Gap',
    palette='Failed spray',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (61, 49, 158), (194, 206, 97), (164, 211, 74), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(80, 80), (200, 80), (200, 200), (80, 200)], fill=accent)
    draw.line((80, 140, 200, 140), fill=bg, width=8)
    draw.line((140, 80, 140, 200), fill=bg, width=8)
    
    return canvas.convert("RGBA")
