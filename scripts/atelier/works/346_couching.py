"""Couched sheet. Independent salon work 346."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=346,
    slug='couching',
    title='Couching',
    description='Wet, transferred, still a drawing.',
    medium='Couched sheet',
    motion='Press',
    palette='Felt rag',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (159, 83, 222), (96, 172, 33), (233, 226, 34), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((90, 90, 300, 400), fill=mid, outline=ink)
    draw.rectangle((220, 140, 430, 440), fill=accent, outline=ink)
    
    return canvas.convert("RGBA")
