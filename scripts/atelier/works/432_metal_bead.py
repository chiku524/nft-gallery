"""Metal bead. Independent salon work 432."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=432,
    slug='metal-bead',
    title='Metal Bead',
    description='Hardware strung.',
    medium='Metal bead',
    motion='Clink',
    palette='Shop bead',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (19, 14, 148), (236, 241, 107), (223, 93, 223), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(9):
        x = 256 + int(8 * math.sin(t + i))
        draw.ellipse((x - 12, 30 + i * 50, x + 12, 54 + i * 50), fill=accent if i % 2 else ink)
    
    return canvas.convert("RGBA")
