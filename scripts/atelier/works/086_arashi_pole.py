"""Arashi shibori. Independent salon work 86."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=86,
    slug='arashi-pole',
    title='Arashi Pole',
    description='Cloth pole-wrapped into weather.',
    medium='Arashi shibori',
    motion='Twist',
    palette='Storm indigo',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (209, 52, 107), (46, 203, 148), (55, 26, 193), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(16):
        y = 20 + i * int(30 * scale) + int(10 * math.sin(t + i))
        draw.arc((40, y, 472, y + 80), 0, 180, fill=ink, width=5)
    
    return canvas.convert("RGBA")
