"""Spinet. Independent salon work 273."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=273,
    slug='tiny-spinet',
    title='Tiny Spinet',
    description='Furniture for a smaller room.',
    medium='Spinet',
    motion='Tinkle',
    palette='Toy ivory',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (187, 112, 108), (12, 12, 14), (27, 113, 174), (99, 62, 61)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((60, 180, 452, 260), fill=ink)
    draw.rectangle((200 + int(40 * math.sin(t)), 160, 280 + int(40 * math.sin(t)), 280), fill=accent)
    
    return canvas.convert("RGBA")
