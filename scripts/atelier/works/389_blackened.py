"""Blackened mail. Independent salon work 389."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=389,
    slug='blackened',
    title='Blackened',
    description='Armor that refuses highlight.',
    medium='Blackened mail',
    motion='Absorb',
    palette='Night iron',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (87, 129, 100), (244, 240, 232), (127, 234, 163), (165, 184, 166)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, (cx, cy) in enumerate(((180, 200), (300, 200), (240, 300), (180, 300), (300, 300))):
        r = 48 + 8 * math.sin(t + i)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ink, width=8)
        draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=accent)
    
    return canvas.convert("RGBA")
