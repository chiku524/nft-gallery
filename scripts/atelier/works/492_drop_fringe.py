"""Bead fringe. Independent salon work 492."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=492,
    slug='drop-fringe',
    title='Drop Fringe',
    description='The belt growing a weather.',
    medium='Bead fringe',
    motion='Hang',
    palette='Fringe glass',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (120, 87, 92), (244, 240, 232), (75, 117, 23), (182, 163, 162)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(12):
        draw.ellipse((200, 20 + i * 40, 312, 48 + i * 40), fill=mid)
        draw.ellipse((230, 28 + i * 40, 250, 48 + i * 40), fill=ink)
        draw.ellipse((262, 28 + i * 40, 282, 48 + i * 40), fill=accent)
    
    return canvas.convert("RGBA")
