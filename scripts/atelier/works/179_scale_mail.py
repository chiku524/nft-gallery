"""Scale mail. Independent salon work 179."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=179,
    slug='scale-mail',
    title='Scale Mail',
    description='Rings pretending they are scales.',
    medium='Scale mail',
    motion='Layer',
    palette='Dragon steel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (118, 64, 79), (137, 191, 176), (28, 159, 167), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(6):
        x = 70 + i * 70
        draw.ellipse((x, 180, x + 64, 360), outline=ink if i % 2 else accent, width=5)
    
    return canvas.convert("RGBA")
