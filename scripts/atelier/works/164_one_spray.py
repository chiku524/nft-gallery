"""Single spray. Independent salon work 164."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=164,
    slug='one-spray',
    title='One Spray',
    description='One pull of the can.',
    medium='Single spray',
    motion='Burst',
    palette='Lone mist',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (148, 175, 115), (12, 12, 14), (182, 193, 29), (80, 93, 64)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((90, 90, 422, 422), fill=ink)
    draw.ellipse((180, 180, 332, 332), fill=bg)
    
    return canvas.convert("RGBA")
