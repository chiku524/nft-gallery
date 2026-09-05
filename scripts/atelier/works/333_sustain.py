"""Sustain pedal. Independent salon work 333."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=333,
    slug='sustain',
    title='Sustain',
    description='A bar that means continue.',
    medium='Sustain pedal',
    motion='Hold',
    palette='Pedal brass',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (243, 144, 194), (12, 111, 61), (134, 236, 145), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 40, 120, 472), fill=ink)
    draw.rectangle((392, 40, 472, 472), fill=ink)
    draw.rectangle((140, 200 + int(30 * math.sin(t)), 372, 280), fill=accent)
    
    return canvas.convert("RGBA")
