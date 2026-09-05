"""Lotus cloisonné. Independent salon work 120."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=120,
    slug='lotus-cell',
    title='Lotus Cell',
    description='A flower that is only partitions.',
    medium='Lotus cloisonné',
    motion='Open',
    palette='Temple enamel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (162, 78, 147), (12, 12, 14), (179, 174, 142), (87, 45, 80)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((100, 100, 412, 412), fill=accent, outline=ink, width=10)
    draw.rectangle((170, 170, 342, 342), fill=mid, outline=ink, width=6)
    
    return canvas.convert("RGBA")
