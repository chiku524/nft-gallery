"""Mezzotint scrape. Independent salon work 110."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=110,
    slug='scrape-light',
    title='Scrape Light',
    description='Light is what you remove.',
    medium='Mezzotint scrape',
    motion='Lift',
    palette='Moon copper',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (206, 135, 85), (49, 120, 170), (220, 125, 127), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.ellipse((160 + ox, 140 + oy, 360, 360), fill=accent)
    
    return canvas.convert("RGBA")
