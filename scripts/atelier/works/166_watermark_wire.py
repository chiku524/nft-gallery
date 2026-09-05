"""Watermark. Independent salon work 166."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=166,
    slug='watermark-wire',
    title='Watermark Wire',
    description='A picture that is only thinner.',
    medium='Watermark',
    motion='Glow',
    palette='Wire pale',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (136, 39, 105), (119, 216, 150), (153, 211, 184), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(40, 80), (470, 60), (450, 450), (70, 430)], fill=mid, outline=ink)
    
    return canvas.convert("RGBA")
