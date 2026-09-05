"""Copper mail. Independent salon work 239."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=239,
    slug='copper-mail',
    title='Copper Mail',
    description='Armor that wants to be a roof.',
    medium='Copper mail',
    motion='Tarnish',
    palette='Penny mail',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (33, 164, 221), (222, 91, 34), (133, 224, 91), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, (cx, cy) in enumerate(((180, 200), (300, 200), (240, 300), (180, 300), (300, 300))):
        r = 48 + 8 * math.sin(t + i)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ink, width=8)
        draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=accent)
    
    return canvas.convert("RGBA")
