"""Cone scale. Independent salon work 143."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=143,
    slug='pine-cone',
    title='Pine Cone',
    description='The tree’s argument, stacked.',
    medium='Cone scale',
    motion='Open',
    palette='Forest rust',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (122, 215, 125), (12, 12, 14), (149, 157, 177), (67, 113, 69)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 70), (420, 400), (90, 400)], fill=mid)
    for i, (x, y) in enumerate(((200, 180), (280, 200), (230, 260), (300, 280), (180, 300))):
        draw.chord((x, y, x + 50, y + 36), 200, 340, fill=accent if i == frame % 5 else ink)
    
    return canvas.convert("RGBA")
