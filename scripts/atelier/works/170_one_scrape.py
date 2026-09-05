"""Single scrape. Independent salon work 170."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=170,
    slug='one-scrape',
    title='One Scrape',
    description='One removal.',
    medium='Single scrape',
    motion='Slash',
    palette='Lone copper',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (200, 192, 147), (55, 63, 108), (70, 83, 105), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.line((80, 400, 400, 90), fill=bg, width=18)
    
    return canvas.convert("RGBA")
