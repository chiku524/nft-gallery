"""Over-spray. Independent salon work 194."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=194,
    slug='over-spray',
    title='Over Spray',
    description='The accident around the law.',
    medium='Over-spray',
    motion='Halo',
    palette='Halo black',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (136, 53, 203), (119, 202, 52), (215, 40, 80), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(80, 80), (200, 80), (200, 200), (80, 200)], fill=accent)
    draw.line((80, 140, 200, 140), fill=bg, width=8)
    draw.line((140, 80, 140, 200), fill=bg, width=8)
    
    return canvas.convert("RGBA")
