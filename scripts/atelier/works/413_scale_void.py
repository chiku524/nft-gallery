"""Missing scale. Independent salon work 413."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=413,
    slug='scale-void',
    title='Scale Void',
    description='The hole is the subject.',
    medium='Missing scale',
    motion='Gap',
    palette='Ink gap',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (47, 169, 181), (208, 86, 74), (52, 30, 116), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    cx, cy = 256 + ox, 300 + oy
    for i in range(8):
        r = int((40 + i * 22) * scale)
        draw.arc((cx - r, cy - r, cx + r, cy + r), 200 + 8 * math.sin(t), 340, fill=ink, width=6)
    
    return canvas.convert("RGBA")
