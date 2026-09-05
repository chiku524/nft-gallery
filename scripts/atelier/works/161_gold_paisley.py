"""Gold paisley. Independent salon work 161."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=161,
    slug='gold-paisley',
    title='Gold Paisley',
    description='A comma in metal.',
    medium='Gold paisley',
    motion='Burnish',
    palette='Brocade gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (211, 245, 179), (44, 10, 76), (228, 116, 122), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.pieslice((150 + ox, 90 + oy, 370 + ox, 420 + oy), 210, 30, fill=ink)
    
    return canvas.convert("RGBA")
