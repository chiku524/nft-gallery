"""Piano key. Independent salon work 63."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=63,
    slug='keybed',
    title='Keybed',
    description='A keyboard with no song, still a walk.',
    medium='Piano key',
    motion='Travel',
    palette='Ivory ebony',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (169, 192, 88), (86, 63, 167), (57, 54, 208), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(14):
        x = 10 + i * 36
        pressed = i == (frame % 14)
        draw.rectangle((x, 80, x + 32, 430), fill=bg if not pressed else accent, outline=ink, width=3)
    for i, n in enumerate((1, 2, 4, 5, 6, 8, 9, 11, 12)):
        x = 32 + n * 36
        draw.rectangle((x, 80, x + 22, 250), fill=ink)
    
    return canvas.convert("RGBA")
