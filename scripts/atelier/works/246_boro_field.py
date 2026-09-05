"""Boro. Independent salon work 246."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=246,
    slug='boro-field',
    title='Boro Field',
    description='Patches that outlived the garment.',
    medium='Boro',
    motion='Patch',
    palette='Mended indigo',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (43, 38, 132), (212, 217, 123), (233, 108, 34), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for i in range(10):
        for j in range(10):
            cx, cy = 50 + i * 44, 50 + j * 44
            draw.arc((cx - 20, cy - 20, cx + 20, cy + 20), 0, 270, fill=ink, width=2)
    
    return canvas.convert("RGBA")
