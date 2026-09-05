"""Gold stencil. Independent salon work 224."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=224,
    slug='gold-stencil',
    title='Gold Stencil',
    description='A crate dressed for a lobby.',
    medium='Gold stencil',
    motion='Flash',
    palette='Show spray',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (182, 135, 42), (73, 120, 213), (37, 168, 126), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.regular_polygon((256 + ox, 256 + oy, int(140 * scale)), 5, rotation=t * 6, fill=ink)
    draw.regular_polygon((256 + ox, 256 + oy, 50), 5, rotation=t * 6, fill=bg)
    
    return canvas.convert("RGBA")
