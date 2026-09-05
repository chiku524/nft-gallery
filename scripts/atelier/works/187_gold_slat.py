"""Gilt blind. Independent salon work 187."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=187,
    slug='gold-slat',
    title='Gold Slat',
    description='Privacy as luxury.',
    medium='Gilt blind',
    motion='Sheen',
    palette='Lobby brass',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (36, 157, 49), (219, 98, 206), (187, 31, 67), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 200, 472, 280), fill=ink)
    draw.rectangle((40, 200, 472, 220), fill=accent)
    
    return canvas.convert("RGBA")
