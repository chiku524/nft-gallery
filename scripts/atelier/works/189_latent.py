"""Latent print. Independent salon work 189."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=189,
    slug='latent',
    title='Latent',
    description='Found, not pressed.',
    medium='Latent print',
    motion='Dust',
    palette='Powder grey',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (39, 18, 116), (216, 237, 139), (94, 76, 222), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((140, 140, 372, 372), outline=ink, width=8)
    draw.ellipse((200, 200, 230, 230), fill=accent)
    
    return canvas.convert("RGBA")
