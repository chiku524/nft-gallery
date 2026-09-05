"""Fresh ogham. Independent salon work 497."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=497,
    slug='new-cut',
    title='New Cut',
    description='The stone still pale at the wound.',
    medium='Fresh ogham',
    motion='Open',
    palette='Fresh grey',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (157, 197, 143), (98, 58, 112), (202, 126, 168), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((256, 80, 256, 432), fill=ink, width=10)
    draw.line((256, 200, 360, 160), fill=accent, width=8)
    
    return canvas.convert("RGBA")
