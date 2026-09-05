"""Dense paisley. Independent salon work 491."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=491,
    slug='overgrown',
    title='Overgrown',
    description='Too many seeds.',
    medium='Dense paisley',
    motion='Crowd',
    palette='Jungle dye',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (236, 199, 150), (19, 56, 105), (239, 66, 70), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(20):
        x, y = 40 + (i * 47) % 420, 40 + (i * 89) % 420
        draw.pieslice((x, y, x + 40, y + 56), 210, 30, fill=accent if i == frame % 20 else ink)
    
    return canvas.convert("RGBA")
