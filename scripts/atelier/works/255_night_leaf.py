"""Night leaf. Independent salon work 255."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=255,
    slug='night-leaf',
    title='Night Leaf',
    description='Gilding after the lamps.',
    medium='Night leaf',
    motion='Dim',
    palette='Void gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (23, 96, 41), (232, 159, 214), (166, 217, 98), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((90, 90, 422, 422), fill=accent)
    draw.rectangle((140, 140, 372, 372), fill=ink)
    
    return canvas.convert("RGBA")
