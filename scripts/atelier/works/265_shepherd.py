"""Shepherd check. Independent salon work 265."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=265,
    slug='shepherd',
    title='Shepherd',
    description='A blanket for weather that never arrives.',
    medium='Shepherd check',
    motion='Fold',
    palette='Flock black',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (122, 226, 82), (133, 29, 173), (124, 139, 200), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=mid)
    for i in range(14):
        p = int(i * 36 * scale)
        draw.line((p, 0, 512, 512 - p), fill=ink, width=3)
        draw.line((0, p, 512 - p, 512), fill=accent, width=2)
    
    return canvas.convert("RGBA")
