"""Night topo. Independent salon work 278."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=278,
    slug='night-survey',
    title='Night Survey',
    description='A map after the office closed.',
    medium='Night topo',
    motion='Glow',
    palette='Moon survey',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (101, 79, 174), (154, 176, 81), (87, 32, 81), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(8):
        r = 40 + i * 24
        draw.ellipse((200 - r, 300 - r, 200 + r, 300 + r), outline=ink, width=2)
        draw.line((200 - 8, 300 + r, 200 + 8, 300 + r), fill=accent, width=2)
    
    return canvas.convert("RGBA")
