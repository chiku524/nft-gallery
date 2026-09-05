"""Black terrazzo. Independent salon work 177."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=177,
    slug='noir-chip',
    title='Noir Chip',
    description='A night floor.',
    medium='Black terrazzo',
    motion='Glint',
    palette='Noir speck',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (169, 153, 233), (86, 102, 22), (218, 71, 239), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(40, 40), (472, 90), (430, 470), (70, 440)], fill=mid)
    draw.polygon([(200, 180), (260, 160), (240, 230)], fill=accent)
    draw.polygon([(300, 300), (360, 280), (340, 350)], fill=ink)
    
    return canvas.convert("RGBA")
