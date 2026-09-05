"""Riveted mail. Independent salon work 119."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=119,
    slug='riveted-mail',
    title='Riveted Mail',
    description='Each ring remembers a hammer.',
    medium='Riveted mail',
    motion='Lock',
    palette='Forge dark',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (230, 200, 183), (25, 55, 72), (125, 136, 201), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((80, 80, 432, 432), outline=ink, width=16)
    draw.ellipse((160, 160, 352, 352), outline=accent, width=10)
    
    return canvas.convert("RGBA")
