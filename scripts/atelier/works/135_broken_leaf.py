"""Broken leaf. Independent salon work 135."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=135,
    slug='broken-leaf',
    title='Broken Leaf',
    description='The leaf failed. The fault is the drawing.',
    medium='Broken leaf',
    motion='Crack',
    palette='Fault gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (195, 234, 173), (60, 21, 82), (117, 237, 208), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(16):
        x, y = 40 + (i * 53) % 420, 40 + (i * 97) % 420
        draw.rectangle((x, y, x + 36, y + 36), fill=ink if i % 2 else accent)
    
    return canvas.convert("RGBA")
