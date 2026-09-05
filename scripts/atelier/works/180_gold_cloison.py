"""Gold cloisonné. Independent salon work 180."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=180,
    slug='gold-cloison',
    title='Gold Cloison',
    description='A small empire.',
    medium='Gold cloisonné',
    motion='Burnish',
    palette='Imperial gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (147, 229, 119), (108, 26, 136), (49, 171, 206), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 60), (430, 200), (370, 430), (140, 430), (80, 200)], fill=mid, outline=ink, width=8)
    draw.ellipse((200, 190, 312, 300), fill=accent)
    
    return canvas.convert("RGBA")
