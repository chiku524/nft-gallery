"""Single cane hex. Independent salon work 169."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=169,
    slug='one-hex-cane',
    title='One Hex Cane',
    description='One hole of a seat.',
    medium='Single cane hex',
    motion='Hold',
    palette='Lone cane',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (188, 50, 77), (67, 205, 178), (143, 22, 239), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((180 + ox, 180 + oy, 332, 332), outline=ink, width=10)
    
    return canvas.convert("RGBA")
