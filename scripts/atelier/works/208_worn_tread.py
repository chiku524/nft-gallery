"""Worn plate. Independent salon work 208."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=208,
    slug='worn-tread',
    title='Worn Tread',
    description='The diamonds are tired.',
    medium='Worn plate',
    motion='Polish',
    palette='Traffic steel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (202, 70, 50), (53, 185, 205), (178, 128, 185), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    step = int(46 * scale)
    for y in range(20, 500, step):
        for x in range(20 + (y // step % 2) * step // 2, 500, step):
            draw.regular_polygon((x, y + int(3 * math.sin(t)), 14), 4, rotation=45, fill=ink)
    
    return canvas.convert("RGBA")
