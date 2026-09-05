"""White wampum. Independent salon work 462."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=462,
    slug='white-shell',
    title='White Shell',
    description='The quiet half of a treaty.',
    medium='White wampum',
    motion='Calm',
    palette='Shell pale',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (142, 17, 119), (113, 238, 136), (66, 44, 74), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(20):
        draw.ellipse((40 + i * 22, 240, 56 + i * 22, 256), fill=ink if i % 2 else accent)
    
    return canvas.convert("RGBA")
