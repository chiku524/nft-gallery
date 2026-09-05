"""Night sgraffito. Independent salon work 481."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=481,
    slug='night-plaster',
    title='Night Plaster',
    description='A wall after the lamps go out.',
    medium='Night sgraffito',
    motion='Score',
    palette='Moon plaster',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (17, 84, 59), (238, 171, 196), (229, 95, 119), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.polygon([(80, 400), (256, 80), (430, 400)], outline=bg, width=8)
    
    return canvas.convert("RGBA")
