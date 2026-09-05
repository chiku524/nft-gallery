"""Caution stencil. Independent salon work 464."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=464,
    slug='caution-stenc',
    title='Caution Stenc',
    description='A warning with no hazard.',
    medium='Caution stencil',
    motion='Warn',
    palette='Shop yellow',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (66, 189, 232), (189, 66, 23), (23, 83, 154), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((90, 90, 422, 422), fill=ink)
    draw.ellipse((180, 180, 332, 332), fill=bg)
    
    return canvas.convert("RGBA")
