"""Vat dip. Independent salon work 376."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=376,
    slug='vatman',
    title='Vatman',
    description='The mould coming up.',
    medium='Vat dip',
    motion='Lift',
    palette='Vat cream',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (161, 47, 61), (94, 208, 194), (142, 223, 93), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    rng = np.random.default_rng(4)
    pts = []
    for i in range(40):
        ang = i / 40 * math.tau
        r = 200 + int(rng.integers(-18, 18))
        pts.append((256 + r * math.cos(ang), 256 + r * math.sin(ang)))
    draw.polygon([(int(x), int(y)) for x, y in pts], fill=mid, outline=ink)
    
    return canvas.convert("RGBA")
