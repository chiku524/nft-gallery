"""Corrugated flute. Independent salon work 70."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=70,
    slug='box-flute',
    title='Box Flute',
    description='A box that forgot its product.',
    medium='Corrugated flute',
    motion='Flex',
    palette='Carton kraft',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (135, 146, 82), (244, 240, 232), (56, 82, 63), (189, 193, 157)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for x in range(0, 512, int(18 * scale)):
        draw.polygon([(x, 0), (x + 8, 0), (x + 8, 512), (x, 512)], fill=ink if (x // 18) % 2 else accent)
    
    return canvas.convert("RGBA")
