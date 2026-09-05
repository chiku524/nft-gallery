"""Organ manual. Independent salon work 183."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=183,
    slug='organ-manual',
    title='Organ Manual',
    description='Stops implied by color alone.',
    medium='Organ manual',
    motion='Stop',
    palette='Church wood',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (217, 39, 222), (38, 216, 33), (62, 83, 166), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 40, 120, 472), fill=ink)
    draw.rectangle((392, 40, 472, 472), fill=ink)
    draw.rectangle((140, 200 + int(30 * math.sin(t)), 372, 280), fill=accent)
    
    return canvas.convert("RGBA")
