"""Pinstripe. Independent salon work 205."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=205,
    slug='pinstripe-run',
    title='Pinstripe Run',
    description='A suit that forgot the body.',
    medium='Pinstripe',
    motion='Stride',
    palette='Bank navy',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (165, 159, 50), (90, 96, 205), (75, 33, 39), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for x in range(0, 512, int(28 * scale)):
        draw.rectangle((x, 0, x + 10, 512), fill=ink)
    for y in range(0, 512, int(36 * scale)):
        draw.rectangle((0, y, 512, y + 8), fill=accent)
    draw.rectangle((0, 0, 512, 512), outline=mid, width=18)
    
    return canvas.convert("RGBA")
