"""Gilding size. Independent salon work 165."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=165,
    slug='varnish-size',
    title='Varnish Size',
    description='The sticky hour before the leaf.',
    medium='Gilding size',
    motion='Tack',
    palette='Size amber',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (149, 118, 103), (244, 240, 232), (156, 135, 113), (196, 179, 167)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((120 + ox, 120 + oy, 392, 392), fill=ink)
    draw.ellipse((200, 200, 310, 310), fill=accent)
    
    return canvas.convert("RGBA")
