"""Delta void. Independent salon work 489."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=489,
    slug='void-center',
    title='Void Center',
    description='The center declined.',
    medium='Delta void',
    motion='Gap',
    palette='Delta ink',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (34, 68, 103), (221, 187, 152), (94, 83, 220), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((140, 140, 372, 372), outline=ink, width=8)
    draw.ellipse((200, 200, 230, 230), fill=accent)
    
    return canvas.convert("RGBA")
