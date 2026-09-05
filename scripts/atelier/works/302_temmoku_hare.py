"""Hare’s fur. Independent salon work 302."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=302,
    slug='temmoku-hare',
    title='Temmoku Hare',
    description='Fur without the animal.',
    medium='Hare’s fur',
    motion='Streak',
    palette='Hare brown',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (228, 64, 131), (27, 191, 124), (181, 28, 121), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 140), fill=ink)
    draw.polygon([(80, 140), (140, 420), (40, 420)], fill=accent)
    draw.polygon([(300, 140), (360, 460), (250, 460)], fill=mid)
    
    return canvas.convert("RGBA")
