"""Koi scale. Independent salon work 113."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=113,
    slug='koi-mail',
    title='Koi Mail',
    description='A fish that is only its weather.',
    medium='Koi scale',
    motion='Swim',
    palette='Vermilion pond',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (62, 245, 64), (193, 10, 191), (162, 51, 235), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    cx, cy = 256 + ox, 300 + oy
    for i in range(8):
        r = int((40 + i * 22) * scale)
        draw.arc((cx - r, cy - r, cx + r, cy + r), 200 + 8 * math.sin(t), 340, fill=ink, width=6)
    
    return canvas.convert("RGBA")
