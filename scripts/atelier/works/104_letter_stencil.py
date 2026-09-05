"""Letter stencil. Independent salon work 104."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=104,
    slug='letter-stencil',
    title='Letter Stencil',
    description='A letter with no word.',
    medium='Letter stencil',
    motion='Index',
    palette='Crate black',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (117, 133, 198), (12, 12, 14), (74, 231, 168), (64, 72, 106)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((80, 80, 200, 400), fill=ink)
    draw.rectangle((140, 140, 180, 200), fill=bg)
    draw.rectangle((140, 240, 180, 340), fill=bg)
    
    return canvas.convert("RGBA")
