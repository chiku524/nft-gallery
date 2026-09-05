"""Higaki. Independent salon work 186."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=186,
    slug='higaki',
    title='Higaki',
    description='A fence drawn with thread.',
    medium='Higaki',
    motion='Fence',
    palette='Cypress stitch',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (45, 70, 51), (210, 185, 204), (132, 162, 193), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    patches = [(60, 60, 220, 240), (200, 180, 400, 360), (120, 300, 340, 460)]
    for box in patches:
        draw.rectangle(box, outline=ink, width=4)
        draw.line((box[0] + 10, box[1] + 20, box[2] - 10, box[1] + 20), fill=accent, width=2)
    
    return canvas.convert("RGBA")
