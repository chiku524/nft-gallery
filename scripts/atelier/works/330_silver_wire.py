"""Silver cloisonné. Independent salon work 330."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=330,
    slug='silver-wire',
    title='Silver Wire',
    description='Cold metal, warm glass.',
    medium='Silver cloisonné',
    motion='Trace',
    palette='Moon enamel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (46, 145, 192), (209, 110, 63), (150, 185, 121), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 60), (430, 200), (370, 430), (140, 430), (80, 200)], fill=mid, outline=ink, width=8)
    draw.ellipse((200, 190, 312, 300), fill=accent)
    
    return canvas.convert("RGBA")
