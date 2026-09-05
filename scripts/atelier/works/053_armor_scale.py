"""Lamellar. Independent salon work 53."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=53,
    slug='armor-scale',
    title='Armor Scale',
    description='A soldier reduced to the idea of overlapping.',
    medium='Lamellar',
    motion='Lift',
    palette='Bronze dusk',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (193, 229, 202), (62, 26, 53), (206, 138, 110), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    step = int(28 * scale)
    for row, y in enumerate(range(20, 520, step)):
        shift = (row % 2) * step // 2 + int(6 * math.sin(t + row))
        for x in range(-20 + shift, 540, step):
            draw.chord((x, y, x + step + 8, y + step + 4), 200, 340, fill=ink if row % 3 else accent, outline=mid)
    
    return canvas.convert("RGBA")
