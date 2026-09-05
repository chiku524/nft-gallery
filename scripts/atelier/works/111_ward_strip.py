"""EKG paper. Independent salon work 111."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=111,
    slug='ward-strip',
    title='Ward Strip',
    description='A heart with no body. The grid is the only furniture.',
    medium='EKG paper',
    motion='Beat',
    palette='Clinical red',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (187, 123, 33), (68, 132, 222), (152, 213, 63), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts = []
    for k in range(240):
        ang = k / 240 * math.tau + t * 0.2
        r = 40 + (160 * scale) + 26 * math.sin(k * 0.35 + t)
        pts.append((256 + ox + r * math.cos(ang), 256 + oy + r * math.sin(ang)))
    draw.line([(int(x), int(y)) for x, y in pts], fill=ink, width=3)
    
    return canvas.convert("RGBA")
