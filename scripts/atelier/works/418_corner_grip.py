"""Tread crop. Independent salon work 418."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=418,
    slug='corner-grip',
    title='Corner Grip',
    description='Only the warning.',
    medium='Tread crop',
    motion='Crop',
    palette='Edge mill',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (226, 220, 116), (29, 35, 139), (234, 39, 221), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.regular_polygon((256 + ox, 256 + oy, int(120 * scale)), 4, rotation=45, fill=ink)
    draw.regular_polygon((256 + ox, 256 + oy, 40), 4, rotation=45 + t * 10, fill=accent)
    
    return canvas.convert("RGBA")
