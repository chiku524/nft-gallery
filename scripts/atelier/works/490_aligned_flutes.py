"""End-on flute. Independent salon work 490."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=490,
    slug='aligned-flutes',
    title='Aligned Flutes',
    description='Looking down the tunnels.',
    medium='End-on flute',
    motion='Aim',
    palette='Tunnel kraft',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (67, 85, 103), (188, 170, 152), (179, 196, 44), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(8):
        x = 40 + i * 56
        draw.arc((x, 80, x + 56, 432), 270, 90, fill=ink if i % 2 else accent, width=8)
    
    return canvas.convert("RGBA")
