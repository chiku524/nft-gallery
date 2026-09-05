"""Miura shibori. Independent salon work 176."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=176,
    slug='miura',
    title='Miura',
    description='Loops that never become rope.',
    medium='Miura shibori',
    motion='Loop',
    palette='Bound blue',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (174, 101, 146), (12, 12, 14), (148, 151, 239), (93, 56, 80)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, int(220 + 40 * math.sin(t))), fill=ink)
    for x in range(20, 500, 18):
        draw.line((x, 0, x + 8, 512), fill=accent, width=2)
    
    return canvas.convert("RGBA")
