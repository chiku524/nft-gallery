"""Mini stencil. Independent salon work 254."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=254,
    slug='tiny-stencil',
    title='Tiny Stencil',
    description='A smaller instruction.',
    medium='Mini stencil',
    motion='Tick',
    palette='Pocket spray',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (223, 114, 185), (32, 141, 70), (118, 45, 157), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((80, 80, 200, 400), fill=ink)
    draw.rectangle((140, 140, 180, 200), fill=bg)
    draw.rectangle((140, 240, 180, 340), fill=bg)
    
    return canvas.convert("RGBA")
