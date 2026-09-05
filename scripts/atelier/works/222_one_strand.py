"""Single strand. Independent salon work 222."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=222,
    slug='one-strand',
    title='One Strand',
    description='One decision, vertical.',
    medium='Single strand',
    motion='Hang',
    palette='Lone bead',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (42, 12, 93), (213, 243, 162), (110, 223, 95), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    colors = [ink, accent, mid, bg]
    for row in range(16):
        for col in range(16):
            x = 24 + col * 30 + (row % 2) * 15
            y = 24 + row * 30
            draw.ellipse((x, y, x + 16, y + 16), fill=colors[(row + col + frame) % 4], outline=ink)
    
    return canvas.convert("RGBA")
