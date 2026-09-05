"""Single slat. Independent salon work 217."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=217,
    slug='one-slat',
    title='One Slat',
    description='One decision about light.',
    medium='Single slat',
    motion='Tilt',
    palette='Lone cream',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (132, 207, 243), (123, 48, 12), (150, 198, 75), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, y in enumerate(range(20, 500, int(22 * scale))):
        tilt = int(10 * math.sin(t + i * 0.2))
        draw.polygon([(20, y), (492, y + tilt), (492, y + 14 + tilt), (20, y + 14)], fill=ink if i % 2 == 0 else accent)
    
    return canvas.convert("RGBA")
