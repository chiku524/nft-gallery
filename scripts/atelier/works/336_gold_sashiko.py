"""Gold sashiko. Independent salon work 336."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=336,
    slug='gold-sashiko',
    title='Gold Sashiko',
    description='Repair as jewelry.',
    medium='Gold sashiko',
    motion='Gleam',
    palette='Gilt indigo',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (142, 42, 180), (113, 213, 75), (150, 64, 151), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    patches = [(60, 60, 220, 240), (200, 180, 400, 360), (120, 300, 340, 460)]
    for box in patches:
        draw.rectangle(box, outline=ink, width=4)
        draw.line((box[0] + 10, box[1] + 20, box[2] - 10, box[1] + 20), fill=accent, width=2)
    
    return canvas.convert("RGBA")
