"""Over-rocked. Independent salon work 350."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=350,
    slug='over-rocked',
    title='Over Rocked',
    description='Too much night.',
    medium='Over-rocked',
    motion='Flood',
    palette='Black flood',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (138, 118, 64), (244, 240, 232), (120, 78, 158), (191, 179, 148)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.ellipse((180, 180, 250, 250), fill=bg)
    draw.ellipse((280, 260, 350, 330), fill=accent)
    
    return canvas.convert("RGBA")
