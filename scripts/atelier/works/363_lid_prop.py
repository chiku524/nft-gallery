"""Piano lid. Independent salon work 363."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=363,
    slug='lid-prop',
    title='Lid Prop',
    description='A mouth.',
    medium='Piano lid',
    motion='Open',
    palette='Lacquer black',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (243, 183, 124), (12, 72, 131), (95, 134, 158), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
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
