"""Ne-maki. Independent salon work 266."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=266,
    slug='ne-maki',
    title='Ne Maki',
    description='Wound from the root out.',
    medium='Ne-maki',
    motion='Wind',
    palette='Root indigo',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (163, 86, 108), (244, 240, 232), (124, 163, 49), (203, 163, 170)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts = [(256, 40), (420, 140), (380, 400), (130, 400), (90, 140)]
    draw.polygon(pts, fill=mid)
    for i, p in enumerate(pts):
        q = pts[(i + 1) % len(pts)]
        draw.line((p[0], p[1], q[0], q[1]), fill=ink, width=10)
    draw.regular_polygon((256 + int(20 * math.sin(t)), 240, 50), 4, fill=accent)
    
    return canvas.convert("RGBA")
