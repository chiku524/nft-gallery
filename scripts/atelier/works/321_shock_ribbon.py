"""Ribbon galvanometer. Independent salon work 321."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=321,
    slug='shock-ribbon',
    title='Shock Ribbon',
    description='Light, not ink — but the paper still takes a scar.',
    medium='Ribbon galvanometer',
    motion='Flick',
    palette='Violet paper',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (228, 12, 35), (27, 243, 220), (143, 208, 102), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((90, 110, 422, 402), outline=ink, width=8)
    pts = []
    for x in range(110, 402):
        y = 256 + int(40 * math.sin(x * 0.12 + t))
        pts.append((x, y))
    draw.line(pts, fill=accent, width=3)
    
    return canvas.convert("RGBA")
