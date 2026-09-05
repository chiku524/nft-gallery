"""Itajime. Independent salon work 116."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=116,
    slug='itajime',
    title='Itajime',
    description='A fold remembered by dye.',
    medium='Itajime',
    motion='Clamp',
    palette='Board indigo',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (140, 59, 38), (115, 196, 217), (151, 183, 120), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts = [(256, 40), (420, 140), (380, 400), (130, 400), (90, 140)]
    draw.polygon(pts, fill=mid)
    for i, p in enumerate(pts):
        q = pts[(i + 1) % len(pts)]
        draw.line((p[0], p[1], q[0], q[1]), fill=ink, width=10)
    draw.regular_polygon((256 + int(20 * math.sin(t)), 240, 50), 4, fill=accent)
    
    return canvas.convert("RGBA")
