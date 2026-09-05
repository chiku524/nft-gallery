"""Sun-faded tartan. Independent salon work 385."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=385,
    slug='faded-sett',
    title='Faded Sett',
    description='The family got tired.',
    medium='Sun-faded tartan',
    motion='Bleach',
    palette='Washed clan',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (117, 210, 186), (138, 45, 69), (158, 175, 202), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    bands = [18, 6, 40, 10, 22]
    x = 0
    for i, w in enumerate(bands * 8):
        draw.rectangle((x, 0, x + w, 512), fill=(ink, accent, mid, bg, ink)[i % 5])
        x += w
    y = int(80 + 40 * math.sin(t))
    draw.rectangle((0, y, 512, y + 26), fill=accent)
    
    return canvas.convert("RGBA")
