"""Celadon drip. Independent salon work 62."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=62,
    slug='celadon-run',
    title='Celadon Run',
    description='The glaze decided to leave.',
    medium='Celadon drip',
    motion='Run',
    palette='Jade kiln',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (112, 171, 104), (12, 12, 14), (118, 20, 232), (62, 91, 59)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, x in enumerate(range(40, 480, int(36 * scale))):
        h = int(180 + 140 * math.sin(t + i) * 0.5 + 80)
        draw.rectangle((x, 20, x + 18, 20 + h), fill=ink if i % 2 else accent)
        draw.ellipse((x - 6, 12 + h, x + 24, 40 + h), fill=ink if i % 2 else accent)
    
    return canvas.convert("RGBA")
