"""Chain line. Independent salon work 136."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=136,
    slug='chain-line',
    title='Chain Line',
    description='The other wires.',
    medium='Chain line',
    motion='Interval',
    palette='Rag interval',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (189, 239, 238), (66, 16, 17), (212, 115, 136), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((70, 70, 442, 442), fill=mid)
    draw.ellipse((180, 180, 332, 332), outline=ink, width=1)
    
    return canvas.convert("RGBA")
