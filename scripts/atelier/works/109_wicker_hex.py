"""Wicker. Independent salon work 109."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=109,
    slug='wicker-hex',
    title='Wicker Hex',
    description='A porch that is only its weave.',
    medium='Wicker',
    motion='Bind',
    palette='Porch cane',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (103, 23, 73), (152, 232, 182), (202, 219, 228), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(12):
        for j in range(12):
            x, y = 20 + i * 40, 20 + j * 40
            draw.arc((x, y, x + 40, y + 40), 0, 180, fill=ink, width=3)
            draw.arc((x + 20, y + 20, x + 60, y + 60), 180, 360, fill=accent, width=3)
    
    return canvas.convert("RGBA")
