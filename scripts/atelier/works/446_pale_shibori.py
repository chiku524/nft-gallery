"""Once-dipped. Independent salon work 446."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=446,
    slug='pale-shibori',
    title='Pale Shibori',
    description='One dip. A rumor of blue.',
    medium='Once-dipped',
    motion='Fade',
    palette='Sky cloth',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (190, 130, 219), (65, 125, 36), (93, 40, 87), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(7):
        r = int((40 + i * 28) * scale)
        draw.ellipse((256 - r + ox, 256 - r + oy, 256 + r + ox, 256 + r + oy), outline=ink, width=4)
    
    return canvas.convert("RGBA")
