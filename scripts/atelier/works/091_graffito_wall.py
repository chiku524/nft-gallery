"""Wall sgraffito. Independent salon work 91."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=91,
    slug='graffito-wall',
    title='Graffito Wall',
    description='A facade that writes on itself.',
    medium='Wall sgraffito',
    motion='Score',
    palette='Plaster umber',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (13, 29, 77), (242, 226, 178), (208, 92, 157), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=mid)
    draw.line((60, 80, 420, 400), fill=ink, width=16)
    draw.line((80, 400, 400, 90), fill=accent, width=10)
    
    return canvas.convert("RGBA")
