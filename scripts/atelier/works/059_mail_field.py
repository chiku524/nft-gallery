"""Chainmail. Independent salon work 59."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=59,
    slug='mail-field',
    title='Mail Field',
    description='A body of rings with no body inside.',
    medium='Chainmail',
    motion='Rattle',
    palette='Armory steel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (197, 82, 108), (58, 173, 147), (35, 77, 193), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    s = int(22 * scale)
    for row in range(18):
        for col in range(18):
            cx = 20 + col * s + (row % 2) * s // 2
            cy = 20 + row * s * 0.72
            r = 10 + 2 * math.sin(t + row)
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ink, width=2)
    
    return canvas.convert("RGBA")
