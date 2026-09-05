"""Versailles parquet. Independent salon work 114."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=114,
    slug='versailles',
    title='Versailles',
    description='A room quoting another room.',
    medium='Versailles parquet',
    motion='Turn',
    palette='Palace oak',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (29, 51, 73), (226, 204, 182), (22, 44, 24), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 60), (452, 256), (256, 452), (60, 256)], outline=ink, width=6)
    for i in range(8):
        r = 40 + i * 22
        draw.rectangle((256 - r, 256 - 8, 256 + r, 256 + 8), outline=accent)
        draw.rectangle((256 - 8, 256 - r, 256 + 8, 256 + r), outline=ink)
    
    return canvas.convert("RGBA")
