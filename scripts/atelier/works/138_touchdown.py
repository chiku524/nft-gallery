"""Touchdown mark. Independent salon work 138."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=138,
    slug='touchdown',
    title='Touchdown',
    description='A place to hit that is only paint.',
    medium='Touchdown mark',
    motion='Mark',
    palette='Aim white',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (53, 186, 118), (202, 69, 137), (180, 169, 234), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 40), (300, 120), (212, 120)], fill=ink)
    draw.polygon([(256, 472), (300, 392), (212, 392)], fill=ink)
    draw.rectangle((248, 140, 264, 372), fill=accent)
    
    return canvas.convert("RGBA")
