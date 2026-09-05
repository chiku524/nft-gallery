"""Ridge count. Independent salon work 429."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=429,
    slug='ridge-count',
    title='Ridge Count',
    description='Counting as a landscape.',
    medium='Ridge count',
    motion='Tally',
    palette='File brown',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (168, 138, 230), (87, 117, 25), (135, 64, 94), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(14):
        draw.arc((60, 140 + i * 12, 452, 360 + i * 12), 200, 340, fill=ink, width=2)
    
    return canvas.convert("RGBA")
