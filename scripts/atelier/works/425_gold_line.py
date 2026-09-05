"""Gold zellige. Independent salon work 425."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=425,
    slug='gold-line',
    title='Gold Line',
    description='The line is the luxury.',
    medium='Gold zellige',
    motion='Trace',
    palette='Gilt tile',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (161, 226, 31), (94, 29, 224), (84, 145, 70), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(12):
        r = 20 + i * 18
        draw.regular_polygon((256, 256, r), 8, rotation=i * 8 + t * 4, outline=ink)
    
    return canvas.convert("RGBA")
