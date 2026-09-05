"""Red sashiko. Independent salon work 486."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=486,
    slug='red-thread',
    title='Red Thread',
    description='A charm stitched as a field.',
    medium='Red sashiko',
    motion='Mark',
    palette='Amulet red',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (199, 206, 214), (56, 49, 41), (96, 182, 100), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    patches = [(60, 60, 220, 240), (200, 180, 400, 360), (120, 300, 340, 460)]
    for box in patches:
        draw.rectangle(box, outline=ink, width=4)
        draw.line((box[0] + 10, box[1] + 20, box[2] - 10, box[1] + 20), fill=accent, width=2)
    
    return canvas.convert("RGBA")
