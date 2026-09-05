"""Rusted plate. Independent salon work 358."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=358,
    slug='rust-tread',
    title='Rust Tread',
    description='The grip is becoming earth.',
    medium='Rusted plate',
    motion='Bloom',
    palette='Yard rust',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (215, 144, 136), (40, 111, 119), (125, 205, 163), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    step = int(46 * scale)
    for y in range(20, 500, step):
        for x in range(20 + (y // step % 2) * step // 2, 500, step):
            draw.regular_polygon((x, y + int(3 * math.sin(t)), 14), 4, rotation=45, fill=ink)
    
    return canvas.convert("RGBA")
