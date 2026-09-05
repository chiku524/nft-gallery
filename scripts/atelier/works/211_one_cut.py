"""Single sgraffito. Independent salon work 211."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=211,
    slug='one-cut',
    title='One Cut',
    description='One decision through two colors.',
    medium='Single sgraffito',
    motion='Slash',
    palette='Lone slip',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (176, 43, 231), (79, 212, 24), (219, 197, 138), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    for i in range(18):
        x0, y0 = 20 + i * 26, 30
        draw.line((x0, y0, x0 + 80, 490), fill=bg, width=3)
    
    return canvas.convert("RGBA")
