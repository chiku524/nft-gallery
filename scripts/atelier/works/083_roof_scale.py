"""Fish-scale shingle. Independent salon work 83."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=83,
    slug='roof-scale',
    title='Roof Scale',
    description='Weather on a wall that never saw rain.',
    medium='Fish-scale shingle',
    motion='Shed',
    palette='Tar silver',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (60, 118, 224), (195, 137, 31), (183, 108, 139), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(9):
        y = 40 + i * 48
        draw.pieslice((80, y, 430, y + 90), 200, 340, fill=ink if i % 2 == 0 else accent, outline=mid)
    
    return canvas.convert("RGBA")
