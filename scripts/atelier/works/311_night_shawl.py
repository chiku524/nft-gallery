"""Night paisley. Independent salon work 311."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=311,
    slug='night-shawl',
    title='Night Shawl',
    description='The shawl after the lamp.',
    medium='Night paisley',
    motion='Dim',
    palette='Moon kashmir',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (177, 148, 92), (12, 12, 14), (174, 185, 89), (94, 80, 53)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.pieslice((150 + ox, 90 + oy, 370 + ox, 420 + oy), 210, 30, fill=ink)
    
    return canvas.convert("RGBA")
