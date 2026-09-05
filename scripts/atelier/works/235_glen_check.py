"""Glen plaid. Independent salon work 235."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=235,
    slug='glen-check',
    title='Glen Check',
    description='Hills turned into a repeat.',
    medium='Glen plaid',
    motion='Step',
    palette='Fog wool',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (207, 137, 201), (48, 118, 54), (89, 22, 188), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    bands = [18, 6, 40, 10, 22]
    x = 0
    for i, w in enumerate(bands * 8):
        draw.rectangle((x, 0, x + w, 512), fill=(ink, accent, mid, bg, ink)[i % 5])
        x += w
    y = int(80 + 40 * math.sin(t))
    draw.rectangle((0, y, 512, y + 26), fill=accent)
    
    return canvas.convert("RGBA")
