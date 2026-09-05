"""Drypoint burr. Independent salon work 410."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=410,
    slug='burr-catch',
    title='Burr Catch',
    description='A different dark — the burr holds ink.',
    medium='Drypoint burr',
    motion='Catch',
    palette='Burr silver',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (135, 33, 38), (120, 222, 217), (174, 79, 203), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.ellipse((160 + ox, 140 + oy, 360, 360), fill=accent)
    
    return canvas.convert("RGBA")
