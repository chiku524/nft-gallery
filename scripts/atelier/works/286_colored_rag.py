"""Colored pulp. Independent salon work 286."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=286,
    slug='colored-rag',
    title='Colored Rag',
    description='The rag already had a past.',
    medium='Colored pulp',
    motion='Tint',
    palette='Mill tint',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (54, 69, 144), (201, 186, 111), (202, 192, 112), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((70, 70, 442, 442), fill=mid)
    draw.ellipse((180, 180, 332, 332), outline=ink, width=1)
    
    return canvas.convert("RGBA")
