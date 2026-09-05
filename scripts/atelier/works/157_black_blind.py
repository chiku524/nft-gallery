"""Black blind. Independent salon work 157."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=157,
    slug='black-blind',
    title='Black Blind',
    description='The room deciding not to see.',
    medium='Black blind',
    motion='Close',
    palette='Noir slat',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (114, 151, 146), (12, 12, 14), (98, 89, 46), (63, 81, 80)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    gap = int(18 + 10 * math.sin(t))
    for y in range(0, 512, 36):
        draw.rectangle((0, y, 512, y + gap), fill=bg)
    
    return canvas.convert("RGBA")
