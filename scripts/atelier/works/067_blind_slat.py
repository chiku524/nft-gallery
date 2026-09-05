"""Venetian blind. Independent salon work 67."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=67,
    slug='blind-slat',
    title='Blind Slat',
    description='A window that is only its refusal.',
    medium='Venetian blind',
    motion='Tilt',
    palette='Office cream',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (159, 236, 153), (96, 19, 102), (99, 149, 41), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, y in enumerate(range(20, 500, int(22 * scale))):
        tilt = int(10 * math.sin(t + i * 0.2))
        draw.polygon([(20, y), (492, y + tilt), (492, y + 14 + tilt), (20, y + 14)], fill=ink if i % 2 == 0 else accent)
    
    return canvas.convert("RGBA")
