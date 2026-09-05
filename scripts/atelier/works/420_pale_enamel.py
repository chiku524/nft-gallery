"""Pale cloisonné. Independent salon work 420."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=420,
    slug='pale-enamel',
    title='Pale Enamel',
    description='Color that almost declined.',
    medium='Pale cloisonné',
    motion='Wash',
    palette='Opal cell',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (161, 242, 59), (94, 13, 196), (49, 197, 123), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((100, 100, 412, 412), fill=accent, outline=ink, width=10)
    draw.rectangle((170, 170, 342, 342), fill=mid, outline=ink, width=6)
    
    return canvas.convert("RGBA")
