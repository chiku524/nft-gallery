"""Empty comb. Independent salon work 232."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=232,
    slug='comb-void',
    title='Comb Void',
    description='The cells are open. The honey already left.',
    medium='Empty comb',
    motion='Drain',
    palette='Wax night',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (241, 200, 22), (14, 55, 233), (175, 36, 191), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    cx, cy, r = 256 + ox, 256 + oy, int(150 * scale)
    rot = t * 0.25 + spin
    pts = [(cx + r * math.cos(k * math.tau / 6 + rot), cy + r * math.sin(k * math.tau / 6 + rot)) for k in range(6)]
    draw.polygon([(int(x), int(y)) for x, y in pts], fill=ink)
    draw.polygon([(int(256 + 70 * math.cos(k * math.tau / 6 + rot)), int(256 + 70 * math.sin(k * math.tau / 6 + rot))) for k in range(6)], fill=accent)
    
    return canvas.convert("RGBA")
