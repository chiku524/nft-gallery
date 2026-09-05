"""Miniature leaf. Independent salon work 315."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=315,
    slug='tiny-book',
    title='Tiny Book',
    description='A smaller icon.',
    medium='Miniature leaf',
    motion='Glint',
    palette='Pocket gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (157, 67, 64), (98, 188, 191), (143, 67, 233), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((120 + ox, 120 + oy, 392, 392), fill=ink)
    draw.ellipse((200, 200, 310, 310), fill=accent)
    
    return canvas.convert("RGBA")
