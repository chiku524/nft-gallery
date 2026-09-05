"""Muqarnas. Independent salon work 73."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=73,
    slug='honeycomb-vault',
    title='Honeycomb Vault',
    description='A ceiling that climbs down.',
    medium='Muqarnas',
    motion='Cascade',
    palette='Vault gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (155, 175, 241), (100, 80, 14), (81, 92, 25), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for row in range(7):
        count = 3 + row
        for col in range(count):
            x = 256 - count * 28 + col * 56
            y = 40 + row * 62
            draw.polygon([(x, y + 50), (x + 24, y), (x + 48, y + 50)], fill=ink if (row + col) % 2 else accent, outline=mid)
    
    return canvas.convert("RGBA")
