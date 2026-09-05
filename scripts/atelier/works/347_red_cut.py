"""Red ogham. Independent salon work 347."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=347,
    slug='red-cut',
    title='Red Cut',
    description='A charm in cuts.',
    medium='Red ogham',
    motion='Mark',
    palette='Amulet score',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (73, 201, 93), (182, 54, 162), (80, 126, 121), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((256, 80, 256, 432), fill=ink, width=10)
    draw.line((256, 200, 360, 160), fill=accent, width=8)
    
    return canvas.convert("RGBA")
