"""Copper red. Independent salon work 212."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=212,
    slug='copper-red',
    title='Copper Red',
    description='A reduction that looks like a blush.',
    medium='Copper red',
    motion='Flush',
    palette='Sacrificial red',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (110, 175, 103), (12, 12, 14), (221, 170, 77), (61, 93, 58)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, x in enumerate(range(40, 480, int(36 * scale))):
        h = int(180 + 140 * math.sin(t + i) * 0.5 + 80)
        draw.rectangle((x, 20, x + 18, 20 + h), fill=ink if i % 2 else accent)
        draw.ellipse((x - 6, 12 + h, x + 24, 40 + h), fill=ink if i % 2 else accent)
    
    return canvas.convert("RGBA")
