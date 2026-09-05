"""Night zellige. Independent salon work 455."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=455,
    slug='night-riad',
    title='Night Riad',
    description='The courtyard after the lamps.',
    medium='Night zellige',
    motion='Dim',
    palette='Moon tile',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (40, 241, 13), (215, 14, 242), (236, 161, 183), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((60, 60, 452, 452), fill=mid)
    draw.regular_polygon((256 + ox, 256 + oy, int(90 * scale)), 8, fill=accent, outline=ink)
    
    return canvas.convert("RGBA")
