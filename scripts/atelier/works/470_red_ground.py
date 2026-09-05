"""Red mezzotint. Independent salon work 470."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=470,
    slug='red-ground',
    title='Red Ground',
    description='Night in another color.',
    medium='Red mezzotint',
    motion='Stain',
    palette='Blood copper',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (53, 24, 15), (202, 231, 240), (87, 159, 35), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.line((80, 400, 400, 90), fill=bg, width=18)
    
    return canvas.convert("RGBA")
