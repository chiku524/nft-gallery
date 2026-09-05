"""Hand-cut zellige. Independent salon work 95."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=95,
    slug='cut-tile',
    title='Cut Tile',
    description='Irregular on purpose.',
    medium='Hand-cut zellige',
    motion='Facet',
    palette='Mosaic mineral',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (20, 59, 53), (235, 196, 202), (73, 61, 79), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts = [(256 + 180 * math.cos(k * math.tau / 8 + t * 0.1), 256 + 180 * math.sin(k * math.tau / 8 + t * 0.1)) for k in range(8)]
    draw.polygon([(int(x), int(y)) for x, y in pts], fill=ink, outline=accent, width=6)
    
    return canvas.convert("RGBA")
