"""Diamond plate. Independent salon work 58."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=58,
    slug='tread-plate',
    title='Tread Plate',
    description='A floor that warns the foot.',
    medium='Diamond plate',
    motion='Grip',
    palette='Shop aluminum',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (218, 55, 92), (37, 200, 163), (156, 185, 197), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    step = int(46 * scale)
    for y in range(20, 500, step):
        for x in range(20 + (y // step % 2) * step // 2, 500, step):
            draw.regular_polygon((x, y + int(3 * math.sin(t)), 14), 4, rotation=45, fill=ink)
    
    return canvas.convert("RGBA")
