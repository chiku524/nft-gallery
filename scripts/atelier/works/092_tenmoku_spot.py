"""Tenmoku. Independent salon work 92."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=92,
    slug='tenmoku-spot',
    title='Tenmoku Spot',
    description='Iron, pooled, then a star.',
    medium='Tenmoku',
    motion='Well',
    palette='Oil-spot black',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (104, 218, 148), (151, 37, 107), (109, 180, 75), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((90, 90, 422, 422), fill=ink)
    draw.ellipse((180, 170, 300, 290), fill=accent)
    
    return canvas.convert("RGBA")
