"""Plan muqarnas. Independent salon work 403."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=403,
    slug='flat-muqarnas',
    title='Flat Muqarnas',
    description='The ceiling, seen from above.',
    medium='Plan muqarnas',
    motion='Plan',
    palette='Draft gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (96, 127, 205), (12, 12, 14), (229, 94, 182), (54, 69, 109)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 80), (400, 220), (330, 400), (180, 400), (110, 220)], fill=mid, outline=ink, width=6)
    draw.polygon([(256, 160), (320, 240), (256, 300), (190, 240)], fill=accent)
    
    return canvas.convert("RGBA")
