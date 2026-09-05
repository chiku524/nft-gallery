"""Night keyboard. Independent salon work 453."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=453,
    slug='night-keyboard',
    title='Night Keyboard',
    description='The keys after the concert.',
    medium='Night keyboard',
    motion='Walk',
    palette='Nocturne',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (113, 33, 242), (142, 222, 13), (237, 22, 45), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((80, 200, 432, 280), fill=mid, outline=ink, width=6)
    draw.ellipse((220, 210, 300, 270), fill=accent)
    
    return canvas.convert("RGBA")
