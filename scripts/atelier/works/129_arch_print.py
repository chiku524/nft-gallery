"""Arch print. Independent salon work 129."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=129,
    slug='arch-print',
    title='Arch Print',
    description='The quietest kind of identity.',
    medium='Arch print',
    motion='Rise',
    palette='Arch ink',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (164, 194, 220), (91, 61, 35), (82, 215, 50), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(14):
        draw.arc((60, 140 + i * 12, 452, 360 + i * 12), 200, 340, fill=ink, width=2)
    
    return canvas.convert("RGBA")
