"""Dense ogham. Independent salon work 257."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=257,
    slug='dense-score',
    title='Dense Score',
    description='Too many names.',
    medium='Dense ogham',
    motion='Crowd',
    palette='Packed score',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (64, 105, 243), (191, 150, 12), (71, 147, 178), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((200, 60, 200, 450), fill=ink, width=8)
    draw.line((200, 180, 320, 140), fill=accent, width=6)
    draw.line((200, 260, 340, 260), fill=accent, width=6)
    
    return canvas.convert("RGBA")
