"""Oilstone cell. Independent salon work 412."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=412,
    slug='oil-cell',
    title='Oil Cell',
    description='A reservoir drawn as if it were polite.',
    medium='Oilstone cell',
    motion='Well',
    palette='Slick umber',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (119, 88, 248), (136, 167, 7), (63, 94, 102), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    s = int(48 * scale)
    for n, (cx, cy) in enumerate(((180, 200), (330, 210), (250, 340))):
        r = s + 10 * math.sin(t + n)
        pts = [(cx + r * math.cos(k * math.tau / 6), cy + r * math.sin(k * math.tau / 6)) for k in range(6)]
        draw.polygon([(int(x), int(y)) for x, y in pts], fill=accent if n == 1 else ink, outline=mid, width=4)
    
    return canvas.convert("RGBA")
