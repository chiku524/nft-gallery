"""Geophone paper. Independent salon work 351."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=351,
    slug='bedrock-tick',
    title='Bedrock Tick',
    description='Listening downward until the line flinches.',
    medium='Geophone paper',
    motion='Tick',
    palette='Ochre dust',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (212, 79, 239), (43, 176, 16), (231, 235, 92), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts = []
    for x in range(24, 488):
        y = 256 + oy + int((70 * scale) * math.sin(x * 0.055 + t) + (28 * scale) * math.sin(x * 0.17 + t * 2))
        pts.append((x + ox // 4, y))
    draw.line(pts, fill=ink, width=max(2, int(3 * scale)))
    
    return canvas.convert("RGBA")
