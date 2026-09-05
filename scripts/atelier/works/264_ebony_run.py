"""Ebony run. Independent salon work 264."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=264,
    slug='ebony-run',
    title='Ebony Run',
    description='Dark wood, one direction.',
    medium='Ebony run',
    motion='Slide',
    palette='Piano black',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (68, 119, 41), (187, 136, 214), (206, 166, 181), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 60), (452, 256), (256, 452), (60, 256)], outline=ink, width=6)
    for i in range(8):
        r = 40 + i * 22
        draw.rectangle((256 - r, 256 - 8, 256 + r, 256 + 8), outline=accent)
        draw.rectangle((256 - 8, 256 - r, 256 + 8, 256 + r), outline=ink)
    
    return canvas.convert("RGBA")
