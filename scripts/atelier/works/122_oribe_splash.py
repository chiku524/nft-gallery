"""Oribe. Independent salon work 122."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=122,
    slug='oribe-splash',
    title='Oribe Splash',
    description='A copper accident kept on purpose.',
    medium='Oribe',
    motion='Splash',
    palette='Oribe green',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (61, 224, 116), (194, 31, 139), (131, 70, 112), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(9):
        x = 60 + i * 48
        draw.line((x, 30, x + int(20 * math.sin(t + i)), 480), fill=ink, width=int(8 * scale))
    
    return canvas.convert("RGBA")
