"""Night stencil. Independent salon work 284."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=284,
    slug='night-spray',
    title='Night Spray',
    description='Sprayed in the dark.',
    medium='Night stencil',
    motion='Mist',
    palette='Void spray',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (14, 95, 238), (241, 160, 17), (116, 231, 133), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(4):
        draw.regular_polygon((130 + i * 90, 256, 40), 5, rotation=t * 4, fill=ink if i % 2 else accent)
    
    return canvas.convert("RGBA")
