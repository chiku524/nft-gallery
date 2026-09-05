"""Clinic terrazzo. Independent salon work 297."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=297,
    slug='hospital-chip',
    title='Hospital Chip',
    description='Hygiene as a pattern.',
    medium='Clinic terrazzo',
    motion='Clean',
    palette='Clinic green',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (135, 51, 145), (244, 240, 232), (188, 100, 70), (189, 145, 188)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((80, 80, 432, 432), fill=mid)
    for i in range(20):
        draw.ellipse((100 + i * 12, 120 + (i * 17) % 200, 130 + i * 12, 150 + (i * 17) % 200), fill=ink)
    
    return canvas.convert("RGBA")
