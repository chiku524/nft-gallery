"""Shadow muqarnas. Independent salon work 433."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=433,
    slug='shadow-cell',
    title='Shadow Cell',
    description='The caves as only their dark.',
    medium='Shadow muqarnas',
    motion='Shade',
    palette='Shade vault',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (180, 89, 154), (75, 166, 101), (171, 222, 55), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.regular_polygon((256, 200, 80), 3, fill=ink)
    draw.regular_polygon((256, 320, 80), 3, rotation=180, fill=accent)
    
    return canvas.convert("RGBA")
