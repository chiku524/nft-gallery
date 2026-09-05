"""Red paisley. Independent salon work 341."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=341,
    slug='red-boteh',
    title='Red Boteh',
    description='A seed that wants to be a heart.',
    medium='Red paisley',
    motion='Pulse',
    palette='Paisley red',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (212, 213, 68), (43, 42, 187), (115, 162, 162), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(20):
        x, y = 40 + (i * 47) % 420, 40 + (i * 89) % 420
        draw.pieslice((x, y, x + 40, y + 56), 210, 30, fill=accent if i == frame % 20 else ink)
    
    return canvas.convert("RGBA")
