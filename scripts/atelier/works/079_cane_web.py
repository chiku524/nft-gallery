"""Cane webbing. Independent salon work 79."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=79,
    slug='cane-web',
    title='Cane Web',
    description='A seat with no chair.',
    medium='Cane webbing',
    motion='Seat',
    palette='Chair cane',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (214, 150, 222), (41, 105, 33), (134, 111, 193), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    s = int(36 * scale)
    for y in range(20, 500, s):
        for x in range(20, 500, s):
            draw.ellipse((x, y, x + s, y + s), outline=ink, width=3)
    
    return canvas.convert("RGBA")
