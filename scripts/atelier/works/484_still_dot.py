"""Spot figure. Independent salon work 484."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=484,
    slug='still-dot',
    title='Still Dot',
    description='The tones agreed to stop. Almost.',
    medium='Spot figure',
    motion='Park',
    palette='Parked beam',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (235, 34, 214), (20, 221, 41), (75, 44, 122), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((240 + int(10 * math.sin(t)), 240, 272, 272), fill=accent)
    draw.rectangle((40, 40, 472, 472), outline=ink, width=2)
    
    return canvas.convert("RGBA")
