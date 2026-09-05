"""Aventail. Independent salon work 329."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=329,
    slug='mail-collar',
    title='Mail Collar',
    description='A neck with no head.',
    medium='Aventail',
    motion='Hang',
    palette='Helm steel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (209, 96, 167), (46, 159, 88), (235, 63, 30), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(6):
        x = 70 + i * 70
        draw.ellipse((x, 180, x + 64, 360), outline=ink if i % 2 else accent, width=5)
    
    return canvas.convert("RGBA")
