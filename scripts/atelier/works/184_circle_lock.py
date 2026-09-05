"""Locked circle. Independent salon work 184."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=184,
    slug='circle-lock',
    title='Circle Lock',
    description='1:1. A circle that had to be earned.',
    medium='Locked circle',
    motion='Hold',
    palette='Unity amber',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (93, 81, 91), (162, 174, 164), (57, 149, 224), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((240 + int(10 * math.sin(t)), 240, 272, 272), fill=accent)
    draw.rectangle((40, 40, 472, 472), outline=ink, width=2)
    
    return canvas.convert("RGBA")
