"""Single boteh. Independent salon work 131."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=131,
    slug='one-boteh',
    title='One Boteh',
    description='One seed.',
    medium='Single boteh',
    motion='Seat',
    palette='Lone dye',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (81, 234, 28), (174, 21, 227), (97, 140, 74), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(6):
        x = 70 + (i % 3) * 140
        y = 90 + (i // 3) * 180
        draw.pieslice((x, y, x + 120, y + 160), 200, 20, fill=ink if i % 2 else accent)
    
    return canvas.convert("RGBA")
