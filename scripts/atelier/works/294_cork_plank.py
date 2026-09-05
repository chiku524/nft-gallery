"""Cork plank. Independent salon work 294."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=294,
    slug='cork-plank',
    title='Cork Plank',
    description='A floor that remembers feet. No pins.',
    medium='Cork plank',
    motion='Give',
    palette='Tan give',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (12, 230, 87), (243, 25, 168), (183, 227, 154), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, y in enumerate(range(40, 480, int(28 * scale))):
        draw.rectangle((30 + (i % 3) * 8, y, 482, y + 16), fill=ink if i % 2 == 0 else accent)
        draw.line((30, y + 16, 482, y + 16), fill=mid, width=2)
    
    return canvas.convert("RGBA")
