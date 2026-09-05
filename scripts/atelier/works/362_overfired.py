"""Overfired drip. Independent salon work 362."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=362,
    slug='overfired',
    title='Overfired',
    description='Too hot. Still a painting.',
    medium='Overfired drip',
    motion='Boil',
    palette='Blister kiln',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (158, 190, 192), (97, 65, 63), (152, 79, 178), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, x in enumerate(range(40, 480, int(36 * scale))):
        h = int(180 + 140 * math.sin(t + i) * 0.5 + 80)
        draw.rectangle((x, 20, x + 18, 20 + h), fill=ink if i % 2 else accent)
        draw.ellipse((x - 6, 12 + h, x + 24, 40 + h), fill=ink if i % 2 else accent)
    
    return canvas.convert("RGBA")
