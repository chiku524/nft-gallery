"""Wet corrugate. Independent salon work 460."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=460,
    slug='wet-kraft',
    title='Wet Kraft',
    description='The box met weather.',
    medium='Wet corrugate',
    motion='Sag',
    palette='Rain kraft',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (169, 87, 86), (86, 168, 169), (24, 24, 186), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((80, 80, 432, 432), fill=mid)
    for x in range(90, 420, 14):
        draw.line((x, 90, x, 420), fill=ink, width=3)
    
    return canvas.convert("RGBA")
