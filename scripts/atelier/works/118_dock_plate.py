"""Dock plate. Independent salon work 118."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=118,
    slug='dock-plate',
    title='Dock Plate',
    description='Cargo without the ship.',
    medium='Dock plate',
    motion='Load',
    palette='Harbor steel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (39, 231, 166), (216, 24, 89), (186, 227, 119), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.regular_polygon((256 + ox, 256 + oy, int(120 * scale)), 4, rotation=45, fill=ink)
    draw.regular_polygon((256 + ox, 256 + oy, 40), 4, rotation=45 + t * 10, fill=accent)
    
    return canvas.convert("RGBA")
