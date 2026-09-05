"""Key crop. Independent salon work 423."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=423,
    slug='key-crop',
    title='Key Crop',
    description='Only a few decisions.',
    medium='Key crop',
    motion='Crop',
    palette='Ivory edge',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (146, 37, 168), (109, 218, 87), (200, 120, 223), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((60, 180, 452, 260), fill=ink)
    draw.rectangle((200 + int(40 * math.sin(t)), 160, 280 + int(40 * math.sin(t)), 280), fill=accent)
    
    return canvas.convert("RGBA")
