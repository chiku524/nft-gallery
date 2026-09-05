"""Number stencil. Independent salon work 494."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=494,
    slug='number-plate',
    title='Number Plate',
    description='A digit that forgot its lot.',
    medium='Number stencil',
    motion='Count',
    palette='Lot white',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (199, 109, 99), (56, 146, 156), (220, 198, 129), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(80, 80), (200, 80), (200, 200), (80, 200)], fill=accent)
    draw.line((80, 140, 200, 140), fill=bg, width=8)
    draw.line((140, 80, 140, 200), fill=bg, width=8)
    
    return canvas.convert("RGBA")
