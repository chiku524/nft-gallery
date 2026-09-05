"""Wampum. Independent salon work 162."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=162,
    slug='wampum',
    title='Wampum',
    description='A treaty with no parties named.',
    medium='Wampum',
    motion='Treaty',
    palette='Shell purple',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (234, 100, 65), (21, 155, 190), (159, 114, 69), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(20):
        draw.ellipse((40 + i * 22, 240, 56 + i * 22, 256), fill=ink if i % 2 else accent)
    
    return canvas.convert("RGBA")
