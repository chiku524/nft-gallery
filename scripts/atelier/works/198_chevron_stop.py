"""Blast chevron. Independent salon work 198."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=198,
    slug='chevron-stop',
    title='Chevron Stop',
    description='Do not go further.',
    medium='Blast chevron',
    motion='Stop',
    palette='Blast yellow',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (174, 80, 83), (81, 175, 172), (49, 88, 239), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((80, 80, 432, 432), fill=ink, width=18)
    draw.line((120, 80, 472, 432), fill=accent, width=8)
    draw.line((200, 180, 312, 292), fill=bg, width=10)
    
    return canvas.convert("RGBA")
