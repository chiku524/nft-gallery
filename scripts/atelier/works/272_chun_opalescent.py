"""Jun glaze. Independent salon work 272."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=272,
    slug='chun-opalescent',
    title='Chun Opalescent',
    description='A sky trapped in a bowl that is not here.',
    medium='Jun glaze',
    motion='Opalesce',
    palette='Jun blue',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (240, 161, 97), (15, 94, 158), (74, 48, 176), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(9):
        x = 60 + i * 48
        draw.line((x, 30, x + int(20 * math.sin(t + i)), 480), fill=ink, width=int(8 * scale))
    
    return canvas.convert("RGBA")
