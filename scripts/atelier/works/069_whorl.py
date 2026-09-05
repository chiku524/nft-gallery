"""Fingerprint whorl. Independent salon work 69."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=69,
    slug='whorl',
    title='Whorl',
    description='An identity with no person.',
    medium='Fingerprint whorl',
    motion='Turn',
    palette='Ink pad',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (43, 89, 35), (212, 166, 220), (70, 100, 63), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for ring in range(10, int(180 * scale), 8):
        draw.ellipse((256 - ring + ox, 256 - ring + oy, 256 + ring + ox, 256 + ring + oy), outline=ink, width=2)
    
    return canvas.convert("RGBA")
