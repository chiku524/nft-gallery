"""Worn parquet. Independent salon work 384."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=384,
    slug='worn-path',
    title='Worn Path',
    description='The walk is the drawing.',
    medium='Worn parquet',
    motion='Fade',
    palette='Traffic oak',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (233, 208, 216), (22, 47, 39), (230, 174, 60), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    s = int(36 * scale)
    for y in range(16, 500, s):
        for x in range(16, 500, s):
            draw.rectangle((x, y, x + s - 4, y + s - 4), fill=ink if (x // s + y // s) % 2 else mid, outline=accent)
    
    return canvas.convert("RGBA")
