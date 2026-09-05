"""Micro paisley. Independent salon work 221."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=221,
    slug='tiny-boteh',
    title='Tiny Boteh',
    description='A smaller swagger.',
    medium='Micro paisley',
    motion='Speck',
    palette='Pocket dye',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (119, 52, 94), (136, 203, 161), (156, 92, 80), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    def boteh(cx, cy, s, rot):
        pts = []
        for k in range(24):
            u = k / 24 * math.tau
            r = s * (0.65 + 0.35 * math.sin(u))
            x = cx + r * math.cos(u + rot)
            y = cy + r * math.sin(u + rot) - s * 0.35 * math.sin(u)
            pts.append((x, y))
        draw.polygon([(int(x), int(y)) for x, y in pts], fill=ink, outline=accent)
    for i, (cx, cy) in enumerate(((180, 180), (320, 220), (240, 340), (360, 360), (140, 320))):
        boteh(cx + ox // 4, cy + oy // 4, 48 * scale, t * 0.2 + i)
    
    return canvas.convert("RGBA")
