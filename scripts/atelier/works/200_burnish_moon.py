"""Burnished mezzotint. Independent salon work 200."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=200,
    slug='burnish-moon',
    title='Burnish Moon',
    description='A moon made by rubbing.',
    medium='Burnished mezzotint',
    motion='Polish',
    palette='Moon plate',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (100, 193, 48), (155, 62, 207), (59, 116, 27), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.ellipse((180, 180, 250, 250), fill=bg)
    draw.ellipse((280, 260, 350, 330), fill=accent)
    
    return canvas.convert("RGBA")
