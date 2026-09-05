"""Closed runway. Independent salon work 438."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=438,
    slug='closed-x',
    title='Closed X',
    description='Do not land.',
    medium='Closed runway',
    motion='Cancel',
    palette='Closed white',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (104, 140, 102), (244, 240, 232), (115, 229, 81), (174, 190, 167)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 40), (300, 120), (212, 120)], fill=ink)
    draw.polygon([(256, 472), (300, 392), (212, 392)], fill=ink)
    draw.rectangle((248, 140, 264, 372), fill=accent)
    
    return canvas.convert("RGBA")
