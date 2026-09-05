"""Laid paper. Independent salon work 106."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=106,
    slug='laid-line',
    title='Laid Line',
    description='Wires remembered by pulp.',
    medium='Laid paper',
    motion='Wire',
    palette='Rag blue',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (80, 233, 175), (175, 22, 80), (97, 115, 131), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for x in range(40, 480, 18):
        draw.line((x, 40, x, 472), fill=ink, width=1)
    for x in range(40, 480, 72):
        draw.line((x, 40, x, 472), fill=accent, width=3)
    
    return canvas.convert("RGBA")
