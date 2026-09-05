"""Broken mail. Independent salon work 209."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=209,
    slug='void-mail',
    title='Void Mail',
    description='The wound is a missing circle.',
    medium='Broken mail',
    motion='Gap',
    palette='Missing ring',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (229, 207, 246), (26, 48, 9), (172, 63, 20), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    s = int(22 * scale)
    for row in range(18):
        for col in range(18):
            cx = 20 + col * s + (row % 2) * s // 2
            cy = 20 + row * s * 0.72
            r = 10 + 2 * math.sin(t + row)
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ink, width=2)
    
    return canvas.convert("RGBA")
