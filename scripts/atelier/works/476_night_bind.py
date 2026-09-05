"""Night shibori. Independent salon work 476."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=476,
    slug='night-bind',
    title='Night Bind',
    description='Tied in the dark on purpose.',
    medium='Night shibori',
    motion='Bind',
    palette='Ink vat',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (79, 16, 41), (176, 239, 214), (61, 146, 123), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, int(220 + 40 * math.sin(t))), fill=ink)
    for x in range(20, 500, 18):
        draw.line((x, 0, x + 8, 512), fill=accent, width=2)
    
    return canvas.convert("RGBA")
