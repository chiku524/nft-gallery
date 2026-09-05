"""Gingham. Independent salon work 175."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=175,
    slug='gingham-field',
    title='Gingham Field',
    description='A tablecloth promoted.',
    medium='Gingham',
    motion='Picnic',
    palette='Picnic red',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (36, 135, 91), (219, 120, 164), (25, 142, 149), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 30), (480, 256), (256, 482), (32, 256)], fill=ink)
    for i in range(-6, 7):
        draw.line((256 + i * 28, 30, 256 + i * 28, 482), fill=accent, width=2)
        draw.line((30, 256 + i * 28, 482, 256 + i * 28), fill=bg, width=2)
    
    return canvas.convert("RGBA")
