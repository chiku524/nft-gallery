"""Mono paisley. Independent salon work 191."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=191,
    slug='mono-paisley',
    title='Mono Paisley',
    description='No color, still a swagger.',
    medium='Mono paisley',
    motion='Stamp',
    palette='Ink boteh',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (63, 204, 213), (192, 51, 42), (149, 58, 202), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(20):
        x, y = 40 + (i * 47) % 420, 40 + (i * 89) % 420
        draw.pieslice((x, y, x + 40, y + 56), 210, 30, fill=accent if i == frame % 20 else ink)
    
    return canvas.convert("RGBA")
