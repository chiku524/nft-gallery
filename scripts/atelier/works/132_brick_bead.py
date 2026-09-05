"""Brick stitch. Independent salon work 132."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=132,
    slug='brick-bead',
    title='Brick Bead',
    description='Beads pretending they are a wall.',
    medium='Brick stitch',
    motion='Bond',
    palette='Bead clay',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (120, 132, 111), (244, 240, 232), (111, 60, 34), (182, 186, 171)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(9):
        x = 256 + int(8 * math.sin(t + i))
        draw.ellipse((x - 12, 30 + i * 50, x + 12, 54 + i * 50), fill=accent if i % 2 else ink)
    
    return canvas.convert("RGBA")
