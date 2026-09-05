"""Red-figure scratch. Independent salon work 151."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=151,
    slug='white-on-red',
    title='White on Red',
    description='A vase grammar without the vase.',
    medium='Red-figure scratch',
    motion='Reveal',
    palette='Pot red',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (248, 105, 99), (7, 150, 156), (75, 223, 79), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((60, 60, 452, 452), fill=ink)
    draw.arc((100, 100, 412, 412), 20 + t * 10, 200, fill=bg, width=12)
    
    return canvas.convert("RGBA")
