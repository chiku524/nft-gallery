"""Vessel lip. Independent salon work 422."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=422,
    slug='lip-run',
    title='Lip Run',
    description='The pour over the edge.',
    medium='Vessel lip',
    motion='Spill',
    palette='Rim glaze',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (228, 63, 34), (27, 192, 221), (190, 161, 93), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(9):
        x = 60 + i * 48
        draw.line((x, 30, x + int(20 * math.sin(t + i)), 480), fill=ink, width=int(8 * scale))
    
    return canvas.convert("RGBA")
