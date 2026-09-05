"""Ground terrazzo. Independent salon work 447."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=447,
    slug='wet-grind',
    title='Wet Grind',
    description='The grinder is still in the room.',
    medium='Ground terrazzo',
    motion='Polish',
    palette='Wet stone',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (19, 85, 207), (236, 170, 48), (110, 223, 122), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((80, 80, 432, 432), fill=mid)
    for i in range(20):
        draw.ellipse((100 + i * 12, 120 + (i * 17) % 200, 130 + i * 12, 150 + (i * 17) % 200), fill=ink)
    
    return canvas.convert("RGBA")
