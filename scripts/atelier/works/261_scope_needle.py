"""Medical scope. Independent salon work 261."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=261,
    slug='scope-needle',
    title='Scope Needle',
    description='Not a radar. A pulse that forgot the patient.',
    medium='Medical scope',
    motion='Scan',
    palette='Green ward',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (45, 64, 165), (210, 191, 90), (82, 164, 149), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts = []
    for k in range(240):
        ang = k / 240 * math.tau + t * 0.2
        r = 40 + (160 * scale) + 26 * math.sin(k * 0.35 + t)
        pts.append((256 + ox + r * math.cos(ang), 256 + oy + r * math.sin(ang)))
    draw.line([(int(x), int(y)) for x, y in pts], fill=ink, width=3)
    
    return canvas.convert("RGBA")
