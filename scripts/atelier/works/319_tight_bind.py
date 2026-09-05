"""Tight cane. Independent salon work 319."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=319,
    slug='tight-bind',
    title='Tight Bind',
    description='No air left.',
    medium='Tight cane',
    motion='Tension',
    palette='Work cane',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (224, 190, 70), (31, 65, 185), (213, 117, 37), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((180 + ox, 180 + oy, 332, 332), outline=ink, width=10)
    
    return canvas.convert("RGBA")
