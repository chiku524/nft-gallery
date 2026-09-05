"""Corflute. Independent salon work 430."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=430,
    slug='plastic-flute',
    title='Plastic Flute',
    description='A sign that used to campaign.',
    medium='Corflute',
    motion='Flex',
    palette='Yard blue',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (238, 148, 228), (17, 107, 27), (163, 217, 59), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, y in enumerate(range(0, 512, 16)):
        draw.rectangle((0, y, 512, y + 8), fill=ink if i % 2 else mid)
    
    return canvas.convert("RGBA")
