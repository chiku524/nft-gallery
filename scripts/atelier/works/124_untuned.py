"""Detuned figure. Independent salon work 124."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=124,
    slug='untuned',
    title='Untuned',
    description='The lock is lost. The drawing continues.',
    medium='Detuned figure',
    motion='Drift',
    palette='Slip amber',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (170, 173, 134), (12, 12, 14), (138, 172, 88), (91, 92, 74)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((96, 96, 416, 416), outline=ink, width=6)
    
    return canvas.convert("RGBA")
