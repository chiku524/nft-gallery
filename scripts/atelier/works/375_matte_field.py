"""Matte leaf. Independent salon work 375."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=375,
    slug='matte-field',
    title='Matte Field',
    description='Gold that refused to shine.',
    medium='Matte leaf',
    motion='Flat',
    palette='Matte gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (239, 58, 185), (16, 197, 70), (128, 119, 126), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((60, 60, 452, 452), fill=ink)
    crack = int(40 * math.sin(t))
    draw.line((60, 200 + crack, 452, 280 - crack), fill=bg, width=3)
    draw.line((200, 60, 260, 452), fill=bg, width=2)
    
    return canvas.convert("RGBA")
