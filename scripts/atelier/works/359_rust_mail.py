"""Rusted mail. Independent salon work 359."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=359,
    slug='rust-mail',
    title='Rust Mail',
    description='Pulled from water and not cleaned.',
    medium='Rusted mail',
    motion='Bloom',
    palette='Bog iron',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (176, 114, 161), (12, 12, 14), (123, 40, 26), (94, 63, 87)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
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
