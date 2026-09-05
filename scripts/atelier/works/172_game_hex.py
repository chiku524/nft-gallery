"""Wargame hex. Independent salon work 172."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=172,
    slug='game-hex',
    title='Game Hex',
    description='A campaign with no pieces, only the board breathing.',
    medium='Wargame hex',
    motion='Advance',
    palette='Olive map',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (78, 153, 114), (244, 240, 232), (91, 95, 236), (161, 196, 173)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 40, 472, 472), outline=ink, width=6)
    r = int(90 * scale)
    draw.regular_polygon((256 + ox, 256 + oy, r), 6, rotation=t * 8, fill=accent, outline=ink)
    
    return canvas.convert("RGBA")
