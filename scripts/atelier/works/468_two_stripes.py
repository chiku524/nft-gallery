"""Paired centerline. Independent salon work 468."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=468,
    slug='two-stripes',
    title='Two Stripes',
    description='Two directions conferring.',
    medium='Paired centerline',
    motion='Split',
    palette='Twin yellow',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (16, 64, 111), (239, 191, 144), (234, 79, 208), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((60, 80, 200, 200, 80, 340, 240, 430), fill=ink, width=14)
    draw.regular_polygon((240, 430, 16), 4, rotation=45, fill=accent)
    
    return canvas.convert("RGBA")
