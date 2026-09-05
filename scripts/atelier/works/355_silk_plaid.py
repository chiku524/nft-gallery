"""Silk plaid. Independent salon work 355."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=355,
    slug='silk-plaid',
    title='Silk Plaid',
    description='Light doing the weaving.',
    medium='Silk plaid',
    motion='Sheen',
    palette='Opera plaid',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (162, 203, 151), (93, 52, 104), (87, 53, 69), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for x in range(0, 512, int(28 * scale)):
        draw.rectangle((x, 0, x + 10, 512), fill=ink)
    for y in range(0, 512, int(36 * scale)):
        draw.rectangle((0, y, 512, y + 8), fill=accent)
    draw.rectangle((0, 0, 512, 512), outline=mid, width=18)
    
    return canvas.convert("RGBA")
