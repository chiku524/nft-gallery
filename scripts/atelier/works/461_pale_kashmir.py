"""Pale paisley. Independent salon work 461."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=461,
    slug='pale-kashmir',
    title='Pale Kashmir',
    description='A rumor of a shawl.',
    medium='Pale paisley',
    motion='Wash',
    palette='Mist dye',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (120, 39, 88), (135, 216, 167), (127, 227, 206), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.pieslice((150 + ox, 90 + oy, 370 + ox, 420 + oy), 210, 30, fill=ink)
    
    return canvas.convert("RGBA")
