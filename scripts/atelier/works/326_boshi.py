"""Boshi shibori. Independent salon work 326."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=326,
    slug='boshi',
    title='Boshi',
    description='A resist that behaves like a hat.',
    medium='Boshi shibori',
    motion='Cap',
    palette='Capped white',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (200, 134, 172), (55, 121, 83), (140, 134, 51), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, int(220 + 40 * math.sin(t))), fill=ink)
    for x in range(20, 500, 18):
        draw.line((x, 0, x + 8, 512), fill=accent, width=2)
    
    return canvas.convert("RGBA")
