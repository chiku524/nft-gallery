"""Inlaid sgraffito. Independent salon work 451."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=451,
    slug='inlaid-cut',
    title='Inlaid Cut',
    description='The scratch, filled again, still a scar.',
    medium='Inlaid sgraffito',
    motion='Fill',
    palette='Inlay clay',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (31, 25, 131), (224, 230, 124), (89, 112, 142), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((60, 60, 452, 452), fill=ink)
    draw.arc((100, 100, 412, 412), 20 + t * 10, 200, fill=bg, width=12)
    
    return canvas.convert("RGBA")
