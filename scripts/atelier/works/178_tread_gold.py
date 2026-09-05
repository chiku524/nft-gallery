"""Gilt tread. Independent salon work 178."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=178,
    slug='tread-gold',
    title='Tread Gold',
    description='Utility dressed for a lobby.',
    medium='Gilt tread',
    motion='Flash',
    palette='Show plate',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (153, 143, 230), (102, 112, 25), (77, 180, 139), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((30, 30, 482, 482), outline=ink, width=12)
    draw.regular_polygon((256, 256, 90), 4, rotation=45, fill=accent)
    
    return canvas.convert("RGBA")
