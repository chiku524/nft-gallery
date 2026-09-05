"""Deep ogham. Independent salon work 437."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=437,
    slug='incised-deep',
    title='Incised Deep',
    description='The tool was sure.',
    medium='Deep ogham',
    motion='Gouge',
    palette='Deep score',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (171, 196, 187), (84, 59, 68), (152, 60, 208), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for x in (160, 256, 352):
        draw.line((x, 50, x, 460), fill=ink, width=5)
        for i in range(8):
            y = 70 + i * 48
            draw.line((x - 30, y, x + 30, y - 12), fill=accent, width=3)
    
    return canvas.convert("RGBA")
