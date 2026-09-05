"""Red pad. Independent salon work 339."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=339,
    slug='red-ink',
    title='Red Ink',
    description='Bureaucracy as a fingertip.',
    medium='Red pad',
    motion='Stamp',
    palette='Official red',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (39, 110, 64), (216, 145, 191), (46, 181, 110), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((140, 140, 372, 372), outline=ink, width=8)
    draw.ellipse((200, 200, 230, 230), fill=accent)
    
    return canvas.convert("RGBA")
