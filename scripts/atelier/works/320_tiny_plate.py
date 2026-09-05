"""Miniature mezzotint. Independent salon work 320."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=320,
    slug='tiny-plate',
    title='Tiny Plate',
    description='A smaller dark.',
    medium='Miniature mezzotint',
    motion='Glint',
    palette='Pocket copper',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (216, 185, 88), (39, 70, 167), (166, 202, 206), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.line((80, 400, 400, 90), fill=bg, width=18)
    
    return canvas.convert("RGBA")
