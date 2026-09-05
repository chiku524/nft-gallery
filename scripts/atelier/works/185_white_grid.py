"""White zellige. Independent salon work 185."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=185,
    slug='white-grid',
    title='White Grid',
    description='Almost silence.',
    medium='White zellige',
    motion='Calm',
    palette='Riad white',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (184, 154, 36), (71, 101, 219), (179, 219, 94), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for k in range(6):
        ang = k * math.tau / 6
        draw.regular_polygon((256 + 120 * math.cos(ang), 256 + 120 * math.sin(ang), 40), 8, fill=ink if k % 2 else accent)
    
    return canvas.convert("RGBA")
