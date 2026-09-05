"""Blind crop. Independent salon work 397."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=397,
    slug='tilt-crop',
    title='Tilt Crop',
    description='A fragment of a refusal.',
    medium='Blind crop',
    motion='Crop',
    palette='Edge cream',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (12, 133, 13), (243, 122, 242), (149, 240, 156), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, x in enumerate(range(30, 490, 28)):
        draw.rectangle((x, 40, x + 16, 472), fill=ink if i % 2 else mid)
    
    return canvas.convert("RGBA")
