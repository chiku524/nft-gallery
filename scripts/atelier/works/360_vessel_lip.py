"""Vessel cloisonné. Independent salon work 360."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=360,
    slug='vessel-lip',
    title='Vessel Lip',
    description='The rim of a jar that is not here.',
    medium='Vessel cloisonné',
    motion='Rim',
    palette='Vase jewel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (116, 66, 86), (139, 189, 169), (152, 42, 135), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    cells = [(80, 80, 220, 240), (200, 70, 430, 200), (220, 190, 460, 400), (60, 230, 230, 450), (180, 300, 340, 470)]
    for n, box in enumerate(cells):
        draw.rectangle(box, fill=accent if n == frame % 5 else mid, outline=ink, width=5)
    
    return canvas.convert("RGBA")
