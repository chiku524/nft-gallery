"""Kusari. Independent salon work 299."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=299,
    slug='japanese-mail',
    title='Japanese Mail',
    description='Rings in a different grammar.',
    medium='Kusari',
    motion='Drape',
    palette='Kusari ink',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (200, 113, 70), (55, 142, 185), (121, 62, 143), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    r = int(70 * scale)
    draw.ellipse((256 - r + ox, 256 - r + oy, 256 + r + ox, 256 + r + oy), outline=ink, width=14)
    draw.ellipse((256 - 12, 256 - 12, 256 + 12, 256 + 12), fill=accent)
    
    return canvas.convert("RGBA")
