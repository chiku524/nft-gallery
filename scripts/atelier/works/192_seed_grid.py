"""Seed bead. Independent salon work 192."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=192,
    slug='seed-grid',
    title='Seed Grid',
    description='Counting as cloth.',
    medium='Seed bead',
    motion='Tally',
    palette='Seed glass',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (226, 30, 32), (29, 225, 223), (127, 200, 61), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(12):
        draw.ellipse((200, 20 + i * 40, 312, 48 + i * 40), fill=mid)
        draw.ellipse((230, 28 + i * 40, 250, 48 + i * 40), fill=ink)
        draw.ellipse((262, 28 + i * 40, 282, 48 + i * 40), fill=accent)
    
    return canvas.convert("RGBA")
