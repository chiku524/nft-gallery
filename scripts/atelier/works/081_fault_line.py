"""Drum recorder. Independent salon work 81."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=81,
    slug='fault-line',
    title='Fault Line',
    description='The paper keeps a secret the bedrock already spent.',
    medium='Drum recorder',
    motion='Slip',
    palette='Ink bone',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (77, 235, 232), (178, 20, 23), (27, 139, 81), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for row in range(7):
        pts = []
        base = 70 + row * 58
        for x in range(20, 492):
            y = base + int(16 * scale * math.sin(x * 0.08 + t + row))
            pts.append((x, y))
        draw.line(pts, fill=ink if row % 2 == 0 else accent, width=2)
    
    return canvas.convert("RGBA")
