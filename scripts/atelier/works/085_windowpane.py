"""Windowpane check. Independent salon work 85."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=85,
    slug='windowpane',
    title='Windowpane',
    description='A window that is only thread.',
    medium='Windowpane check',
    motion='Frame',
    palette='Suit grey',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (52, 104, 13), (203, 151, 242), (56, 130, 103), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    bands = [18, 6, 40, 10, 22]
    x = 0
    for i, w in enumerate(bands * 8):
        draw.rectangle((x, 0, x + w, 512), fill=(ink, accent, mid, bg, ink)[i % 5])
        x += w
    y = int(80 + 40 * math.sin(t))
    draw.rectangle((0, y, 512, y + 26), fill=accent)
    
    return canvas.convert("RGBA")
