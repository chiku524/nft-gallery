"""Wood ogham. Independent salon work 197."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=197,
    slug='wood-ogham',
    title='Wood Ogham',
    description='A stick that is a sentence.',
    medium='Wood ogham',
    motion='Carve',
    palette='Ogham oak',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (70, 40, 25), (185, 215, 230), (63, 109, 48), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((256, 80, 256, 432), fill=ink, width=10)
    draw.line((256, 200, 360, 160), fill=accent, width=8)
    
    return canvas.convert("RGBA")
