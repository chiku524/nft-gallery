"""Cloisonné. Independent salon work 60."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=60,
    slug='wire-cell',
    title='Wire Cell',
    description='Wires holding color the way a fence holds sheep.',
    medium='Cloisonné',
    motion='Fill',
    palette='Kiln jewel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (155, 80, 103), (244, 240, 232), (137, 23, 199), (199, 160, 167)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    cells = [(80, 80, 220, 240), (200, 70, 430, 200), (220, 190, 460, 400), (60, 230, 230, 450), (180, 300, 340, 470)]
    for n, box in enumerate(cells):
        draw.rectangle(box, fill=accent if n == frame % 5 else mid, outline=ink, width=5)
    
    return canvas.convert("RGBA")
