"""Replacement zellige. Independent salon work 485."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=485,
    slug='repair-tile',
    title='Repair Tile',
    description='The new tile does not match. Good.',
    medium='Replacement zellige',
    motion='Patch',
    palette='Misfit glaze',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (33, 197, 43), (222, 58, 212), (145, 129, 35), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for k in range(6):
        ang = k * math.tau / 6
        draw.regular_polygon((256 + 120 * math.cos(ang), 256 + 120 * math.sin(ang), 40), 8, fill=ink if k % 2 else accent)
    
    return canvas.convert("RGBA")
