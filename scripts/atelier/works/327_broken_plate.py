"""Plate terrazzo. Independent salon work 327."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=327,
    slug='broken-plate',
    title='Broken Plate',
    description='Dinner, recycled into a ground.',
    medium='Plate terrazzo',
    motion='Shard',
    palette='China blue',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (143, 238, 241), (112, 17, 14), (208, 211, 74), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(40, 40), (472, 90), (430, 470), (70, 440)], fill=mid)
    draw.polygon([(200, 180), (260, 160), (240, 230)], fill=accent)
    draw.polygon([(300, 300), (360, 280), (340, 350)], fill=ink)
    
    return canvas.convert("RGBA")
