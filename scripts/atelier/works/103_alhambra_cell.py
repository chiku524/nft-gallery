"""Alhambra muqarnas. Independent salon work 103."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=103,
    slug='alhambra-cell',
    title='Alhambra Cell',
    description='A palace reduced to one stalactite.',
    medium='Alhambra muqarnas',
    motion='Nest',
    palette='Nasrid gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (127, 197, 144), (12, 12, 14), (125, 33, 70), (69, 104, 79)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 80), (400, 220), (330, 400), (180, 400), (110, 220)], fill=mid, outline=ink, width=6)
    draw.polygon([(256, 160), (320, 240), (256, 300), (190, 240)], fill=accent)
    
    return canvas.convert("RGBA")
