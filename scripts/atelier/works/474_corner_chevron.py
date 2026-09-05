"""Chevron crop. Independent salon work 474."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=474,
    slug='corner-chevron',
    title='Corner Chevron',
    description='Only the turn survives.',
    medium='Chevron crop',
    motion='Crop',
    palette='Amber varnish',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (48, 158, 62), (207, 97, 193), (129, 55, 154), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((48, 48, 464, 464), outline=ink, width=10)
    for i in range(6):
        x = 80 + i * 60
        draw.polygon([(x, 140), (x + 40, 200), (x + 40, 360), (x, 300)], fill=accent if i == frame % 6 else ink)
    
    return canvas.convert("RGBA")
