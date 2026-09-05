"""Overcheck. Independent salon work 325."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=325,
    slug='overcheck',
    title='Overcheck',
    description='A grid on a grid, still not a cage.',
    medium='Overcheck',
    motion='Layer',
    palette='Scarlet grid',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (113, 103, 65), (244, 240, 232), (24, 180, 115), (178, 171, 148)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 30), (480, 256), (256, 482), (32, 256)], fill=ink)
    for i in range(-6, 7):
        draw.line((256 + i * 28, 30, 256 + i * 28, 482), fill=accent, width=2)
        draw.line((30, 256 + i * 28, 482, 256 + i * 28), fill=bg, width=2)
    
    return canvas.convert("RGBA")
