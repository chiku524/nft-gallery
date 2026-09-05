"""Single flute. Independent salon work 370."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=370,
    slug='one-ridge',
    title='One Ridge',
    description='One fold of a box.',
    medium='Single flute',
    motion='Hold',
    palette='Lone kraft',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (218, 93, 230), (37, 162, 25), (101, 164, 174), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for x in range(0, 512, int(18 * scale)):
        draw.polygon([(x, 0), (x + 8, 0), (x + 8, 512), (x, 512)], fill=ink if (x // 18) % 2 else accent)
    
    return canvas.convert("RGBA")
