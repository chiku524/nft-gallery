"""Dragon scale. Independent salon work 233."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=233,
    slug='dragon-scale',
    title='Dragon Scale',
    description='Myth as a repeat.',
    medium='Dragon scale',
    motion='Heave',
    palette='Temple green',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (214, 170, 49), (41, 85, 206), (227, 87, 175), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(9):
        y = 40 + i * 48
        draw.pieslice((80, y, 430, y + 90), 200, 340, fill=ink if i % 2 == 0 else accent, outline=mid)
    
    return canvas.convert("RGBA")
