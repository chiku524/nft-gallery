"""Wet runway. Independent salon work 498."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=498,
    slug='wet-tarmac',
    title='Wet Tarmac',
    description='The paint on water.',
    medium='Wet runway',
    motion='Sheen',
    palette='Rain tarmac',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (160, 157, 97), (12, 12, 14), (181, 106, 126), (86, 84, 55)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((80, 80, 432, 432), fill=ink, width=18)
    draw.line((120, 80, 472, 432), fill=accent, width=8)
    draw.line((200, 180, 312, 292), fill=bg, width=10)
    
    return canvas.convert("RGBA")
