"""Madras. Independent salon work 115."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=115,
    slug='madras-cross',
    title='Madras Cross',
    description='The crossings ran in the rain on purpose.',
    medium='Madras',
    motion='Bleed',
    palette='Monsoon dye',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (124, 96, 22), (131, 159, 233), (23, 178, 159), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=mid)
    for i in range(14):
        p = int(i * 36 * scale)
        draw.line((p, 0, 512, 512 - p), fill=ink, width=3)
        draw.line((0, p, 512 - p, 512), fill=accent, width=2)
    
    return canvas.convert("RGBA")
