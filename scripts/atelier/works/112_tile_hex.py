"""Hex tile. Independent salon work 112."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=112,
    slug='tile-hex',
    title='Tile Hex',
    description='A floor that refuses a square.',
    medium='Hex tile',
    motion='Shift',
    palette='Lobby clay',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (86, 127, 58), (169, 128, 197), (238, 71, 229), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    s = int(48 * scale)
    for n, (cx, cy) in enumerate(((180, 200), (330, 210), (250, 340))):
        r = s + 10 * math.sin(t + n)
        pts = [(cx + r * math.cos(k * math.tau / 6), cy + r * math.sin(k * math.tau / 6)) for k in range(6)]
        draw.polygon([(int(x), int(y)) for x, y in pts], fill=accent if n == 1 else ink, outline=mid, width=4)
    
    return canvas.convert("RGBA")
