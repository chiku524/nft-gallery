"""Hachure pit. Independent salon work 128."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=128,
    slug='depression',
    title='Depression',
    description='A hole drawn politely.',
    medium='Hachure pit',
    motion='Sink',
    palette='Pit brown',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (240, 166, 173), (15, 89, 82), (142, 186, 136), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(8):
        r = 40 + i * 24
        draw.ellipse((200 - r, 300 - r, 200 + r, 300 + r), outline=ink, width=2)
        draw.line((200 - 8, 300 + r, 200 + 8, 300 + r), fill=accent, width=2)
    
    return canvas.convert("RGBA")
