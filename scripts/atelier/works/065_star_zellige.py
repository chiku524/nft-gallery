"""Zellige star. Independent salon work 65."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=65,
    slug='star-zellige',
    title='Star Zellige',
    description='A star that is only cuts.',
    medium='Zellige star',
    motion='Lock',
    palette='Fes enamel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (91, 81, 40), (164, 174, 215), (221, 42, 91), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(8):
        for j in range(8):
            cx, cy = 40 + i * 60, 40 + j * 60
            pts = [(cx + 26 * math.cos(k * math.tau / 8 + spin), cy + 26 * math.sin(k * math.tau / 8 + spin)) for k in range(8)]
            draw.polygon([(int(x), int(y)) for x, y in pts], fill=accent if (i + j + frame) % 3 == 0 else ink)
    
    return canvas.convert("RGBA")
