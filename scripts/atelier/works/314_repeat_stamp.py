"""Repeat stencil. Independent salon work 314."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=314,
    slug='repeat-stamp',
    title='Repeat Stamp',
    description='The same order, again.',
    medium='Repeat stencil',
    motion='March',
    palette='Poster spray',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (113, 57, 238), (142, 198, 17), (192, 210, 44), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((90, 90, 422, 422), fill=ink)
    draw.ellipse((180, 180, 332, 332), fill=bg)
    
    return canvas.convert("RGBA")
