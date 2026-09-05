"""Stencil spray. Independent salon work 74."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=74,
    slug='spray-star',
    title='Spray Star',
    description='A star that arrived as weather.',
    medium='Stencil spray',
    motion='Mist',
    palette='Shop star',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (84, 129, 233), (171, 126, 22), (138, 106, 72), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.regular_polygon((256 + ox, 256 + oy, int(140 * scale)), 5, rotation=t * 6, fill=ink)
    draw.regular_polygon((256 + ox, 256 + oy, 50), 5, rotation=t * 6, fill=bg)
    
    return canvas.convert("RGBA")
