"""Black cloisonné. Independent salon work 270."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=270,
    slug='black-ground',
    title='Black Ground',
    description='Night as a setting for wires.',
    medium='Black cloisonné',
    motion='Absorb',
    palette='Lacquer enamel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (244, 81, 166), (11, 174, 89), (130, 46, 188), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((100, 100, 412, 412), fill=accent, outline=ink, width=10)
    draw.rectangle((170, 170, 342, 342), fill=mid, outline=ink, width=6)
    
    return canvas.convert("RGBA")
