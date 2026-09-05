"""Silver leaf. Independent salon work 105."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=105,
    slug='silver-leaf',
    title='Silver Leaf',
    description='Moon, beaten.',
    medium='Silver leaf',
    motion='Lay',
    palette='Icon silver',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (40, 145, 136), (215, 110, 119), (90, 192, 58), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((90, 90, 422, 422), fill=accent)
    draw.rectangle((140, 140, 372, 372), fill=ink)
    
    return canvas.convert("RGBA")
