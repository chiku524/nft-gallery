"""Sashiko crop. Independent salon work 396."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=396,
    slug='corner-mend',
    title='Corner Mend',
    description='A fragment of a jacket.',
    medium='Sashiko crop',
    motion='Crop',
    palette='Edge indigo',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (159, 37, 150), (96, 218, 105), (108, 71, 147), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(10):
        for j in range(10):
            cx, cy = 50 + i * 44, 50 + j * 44
            draw.arc((cx - 20, cy - 20, cx + 20, cy + 20), 0, 270, fill=ink, width=2)
    
    return canvas.convert("RGBA")
