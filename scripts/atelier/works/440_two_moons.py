"""Paired scrape. Independent salon work 440."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=440,
    slug='two-moons',
    title='Two Moons',
    description='Two removals conferring.',
    medium='Paired scrape',
    motion='Face',
    palette='Twin copper',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (156, 180, 55), (99, 75, 200), (240, 53, 186), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    for i in range(40):
        x = 20 + i * 12
        draw.line((x, 20, x + 8, 492), fill=mid, width=1)
    
    return canvas.convert("RGBA")
