"""Boteh crop. Independent salon work 401."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=401,
    slug='crop-curl',
    title='Crop Curl',
    description='Only the hook.',
    medium='Boteh crop',
    motion='Crop',
    palette='Edge dye',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (49, 236, 57), (206, 19, 198), (190, 172, 98), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.pieslice((120, 80, 360, 400), 220, 40, fill=ink)
    draw.ellipse((230, 120, 300, 190), fill=accent)
    
    return canvas.convert("RGBA")
