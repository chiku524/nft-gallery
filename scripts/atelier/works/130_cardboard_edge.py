"""Board edge. Independent salon work 130."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=130,
    slug='cardboard-edge',
    title='Cardboard Edge',
    description='The flute, seen from the cut.',
    medium='Board edge',
    motion='Reveal',
    palette='Kraft stripe',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (119, 46, 166), (136, 209, 89), (142, 126, 129), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, y in enumerate(range(0, 512, 16)):
        draw.rectangle((0, y, 512, y + 8), fill=ink if i % 2 else mid)
    
    return canvas.convert("RGBA")
