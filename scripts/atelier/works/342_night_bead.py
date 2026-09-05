"""Night loom. Independent salon work 342."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=342,
    slug='night-bead',
    title='Night Bead',
    description='Strung in the dark.',
    medium='Night loom',
    motion='Dim',
    palette='Void glass',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (163, 69, 76), (92, 186, 179), (148, 51, 131), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(12):
        draw.ellipse((200, 20 + i * 40, 312, 48 + i * 40), fill=mid)
        draw.ellipse((230, 28 + i * 40, 250, 48 + i * 40), fill=ink)
        draw.ellipse((262, 28 + i * 40, 282, 48 + i * 40), fill=accent)
    
    return canvas.convert("RGBA")
