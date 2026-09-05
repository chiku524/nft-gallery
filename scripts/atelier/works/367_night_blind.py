"""Night blind. Independent salon work 367."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=367,
    slug='night-blind',
    title='Night Blind',
    description='Drawn for a sleep that does not happen.',
    medium='Night blind',
    motion='Close',
    palette='Sleep slat',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (167, 198, 61), (88, 57, 194), (216, 223, 226), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i, y in enumerate(range(20, 500, int(22 * scale))):
        tilt = int(10 * math.sin(t + i * 0.2))
        draw.polygon([(20, y), (492, y + tilt), (492, y + 14 + tilt), (20, y + 14)], fill=ink if i % 2 == 0 else accent)
    
    return canvas.convert("RGBA")
