"""Single ogham. Independent salon work 107."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=107,
    slug='one-letter',
    title='One Letter',
    description='One name.',
    medium='Single ogham',
    motion='Cut',
    palette='Lone score',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (136, 50, 157), (119, 205, 98), (200, 224, 49), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((200, 60, 200, 450), fill=ink, width=8)
    draw.line((200, 180, 320, 140), fill=accent, width=6)
    draw.line((200, 260, 340, 260), fill=accent, width=6)
    
    return canvas.convert("RGBA")
