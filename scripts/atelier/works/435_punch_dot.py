"""Punched leaf. Independent salon work 435."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=435,
    slug='punch-dot',
    title='Punch Dot',
    description='The gold, dotted like a sky.',
    medium='Punched leaf',
    motion='Stamp',
    palette='Tool gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (235, 69, 24), (20, 186, 231), (63, 168, 80), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(16):
        x, y = 40 + (i * 53) % 420, 40 + (i * 97) % 420
        draw.rectangle((x, y, x + 36, y + 36), fill=ink if i % 2 else accent)
    
    return canvas.convert("RGBA")
