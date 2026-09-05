"""Water gilding. Independent salon work 465."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=465,
    slug='water-gild',
    title='Water Gild',
    description='Red clay under a sun.',
    medium='Water gilding',
    motion='Flood',
    palette='Bole red',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (105, 139, 237), (150, 116, 18), (127, 227, 143), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((120 + ox, 120 + oy, 392, 392), fill=ink)
    draw.ellipse((200, 200, 310, 310), fill=accent)
    
    return canvas.convert("RGBA")
