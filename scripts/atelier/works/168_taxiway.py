"""Taxiway yellow. Independent salon work 168."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=168,
    slug='taxiway',
    title='Taxiway',
    description='A path for a plane that is not here.',
    medium='Taxiway yellow',
    motion='Turn',
    palette='Hold short',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (123, 23, 221), (132, 232, 34), (67, 50, 187), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((60, 80, 200, 200, 80, 340, 240, 430), fill=ink, width=14)
    draw.regular_polygon((240, 430, 16), 4, rotation=45, fill=accent)
    
    return canvas.convert("RGBA")
