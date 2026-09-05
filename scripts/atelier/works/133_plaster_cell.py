"""Plaster muqarnas. Independent salon work 133."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=133,
    slug='plaster-cell',
    title='Plaster Cell',
    description='White caves, stacked.',
    medium='Plaster muqarnas',
    motion='Cast',
    palette='Gesso cave',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (45, 190, 187), (210, 65, 68), (29, 58, 239), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.regular_polygon((256, 200, 80), 3, fill=ink)
    draw.regular_polygon((256, 320, 80), 3, rotation=180, fill=accent)
    
    return canvas.convert("RGBA")
