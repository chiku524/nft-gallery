"""Single key. Independent salon work 483."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=483,
    slug='one-key',
    title='One Key',
    description='Middle C with no middle.',
    medium='Single key',
    motion='Depress',
    palette='Lone ivory',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (22, 226, 245), (233, 29, 10), (129, 191, 110), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 40, 120, 472), fill=ink)
    draw.rectangle((392, 40, 472, 472), fill=ink)
    draw.rectangle((140, 200 + int(30 * math.sin(t)), 372, 280), fill=accent)
    
    return canvas.convert("RGBA")
