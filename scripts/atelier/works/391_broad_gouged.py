"""Gouge sgraffito. Independent salon work 391."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=391,
    slug='broad-gouged',
    title='Broad Gouged',
    description='The tool was not polite.',
    medium='Gouge sgraffito',
    motion='Gouge',
    palette='Wide slip',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (215, 109, 229), (40, 146, 26), (77, 131, 53), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=mid)
    draw.line((60, 80, 420, 400), fill=ink, width=16)
    draw.line((80, 400, 400, 90), fill=accent, width=10)
    
    return canvas.convert("RGBA")
