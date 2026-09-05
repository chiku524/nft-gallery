"""Sgraffito crop. Independent salon work 421."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=421,
    slug='corner-scratch',
    title='Corner Scratch',
    description='A fragment of a pot.',
    medium='Sgraffito crop',
    motion='Crop',
    palette='Edge slip',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (214, 58, 47), (41, 197, 208), (154, 240, 77), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 40, 472, 472), fill=ink)
    for y in range(70, 450, int(28 * scale)):
        draw.line((70, y, 440, y + int(20 * math.sin(t + y))), fill=bg, width=2)
    
    return canvas.convert("RGBA")
