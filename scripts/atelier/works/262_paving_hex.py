"""Hex paver. Independent salon work 262."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=262,
    slug='paving-hex',
    title='Paving Hex',
    description='Outdoor geometry brought indoors without permission.',
    medium='Hex paver',
    motion='Settle',
    palette='Garden slate',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (201, 92, 221), (54, 163, 34), (186, 231, 164), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    s = int(48 * scale)
    for n, (cx, cy) in enumerate(((180, 200), (330, 210), (250, 340))):
        r = s + 10 * math.sin(t + n)
        pts = [(cx + r * math.cos(k * math.tau / 6), cy + r * math.sin(k * math.tau / 6)) for k in range(6)]
        draw.polygon([(int(x), int(y)) for x, y in pts], fill=accent if n == 1 else ink, outline=mid, width=4)
    
    return canvas.convert("RGBA")
