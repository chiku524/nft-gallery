"""Nacre. Independent salon work 293."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=293,
    slug='nacre-row',
    title='Nacre Row',
    description='Mother-of-pearl without the animal.',
    medium='Nacre',
    motion='Iridesce',
    palette='Pearl dusk',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (234, 176, 241), (21, 79, 14), (82, 116, 187), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 70), (420, 400), (90, 400)], fill=mid)
    for i, (x, y) in enumerate(((200, 180), (280, 200), (230, 260), (300, 280), (180, 300))):
        draw.chord((x, y, x + 50, y + 36), 200, 340, fill=accent if i == frame % 5 else ink)
    
    return canvas.convert("RGBA")
