"""Nui shibori. Independent salon work 206."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=206,
    slug='nui-resist',
    title='Nui Resist',
    description='The stitch is gone. The absence stayed.',
    medium='Nui shibori',
    motion='Stitch',
    palette='Sewn indigo',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (200, 232, 136), (55, 23, 119), (79, 213, 54), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    step = int(36 * scale)
    for y in range(30, 490, step):
        for x in range(30 + (y // step % 2) * step // 2, 490, step):
            r = int(8 + 5 * math.sin(t + x * 0.02 + y * 0.02))
            draw.ellipse((x - r, y - r, x + r, y + r), fill=ink)
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=bg)
    
    return canvas.convert("RGBA")
