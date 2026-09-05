"""Herringbone oak. Independent salon work 144."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=144,
    slug='herring-floor',
    title='Herring Floor',
    description='Not a tweed. A floor that points.',
    medium='Herringbone oak',
    motion='Walk',
    palette='Walnut cream',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (24, 47, 145), (231, 208, 110), (188, 121, 91), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, y in enumerate(range(40, 480, int(28 * scale))):
        draw.rectangle((30 + (i % 3) * 8, y, 482, y + 16), fill=ink if i % 2 == 0 else accent)
        draw.line((30, y + 16, 482, y + 16), fill=mid, width=2)
    
    return canvas.convert("RGBA")
