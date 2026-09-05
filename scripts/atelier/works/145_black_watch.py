"""Black Watch. Independent salon work 145."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=145,
    slug='black-watch',
    title='Black Watch',
    description='Military cloth without the regiment.',
    medium='Black Watch',
    motion='Hold',
    palette='Night green',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (17, 152, 128), (238, 103, 127), (76, 130, 124), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 40, 472, 472), fill=ink)
    for n in range(8):
        mgn = 60 + n * 22
        draw.rectangle((mgn, mgn, 512 - mgn, 512 - mgn), outline=accent if n % 2 else bg, width=4)
    
    return canvas.convert("RGBA")
