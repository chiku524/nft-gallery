"""Crazed zellige. Independent salon work 245."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=245,
    slug='broken-glaze',
    title='Broken Glaze',
    description='The glaze aged into a second pattern.',
    medium='Crazed zellige',
    motion='Crack',
    palette='Craze mineral',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (125, 118, 119), (244, 240, 232), (104, 133, 146), (184, 179, 175)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts = [(256 + 180 * math.cos(k * math.tau / 8 + t * 0.1), 256 + 180 * math.sin(k * math.tau / 8 + t * 0.1)) for k in range(8)]
    draw.polygon([(int(x), int(y)) for x, y in pts], fill=ink, outline=accent, width=6)
    
    return canvas.convert("RGBA")
