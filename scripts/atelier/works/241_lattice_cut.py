"""Lattice sgraffito. Independent salon work 241."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=241,
    slug='lattice-cut',
    title='Lattice Cut',
    description='A fence cut into clay.',
    medium='Lattice sgraffito',
    motion='Grid',
    palette='Garden slip',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (210, 121, 128), (12, 12, 14), (132, 75, 186), (111, 66, 71)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=mid)
    draw.line((60, 80, 420, 400), fill=ink, width=16)
    draw.line((80, 400, 400, 90), fill=accent, width=10)
    
    return canvas.convert("RGBA")
