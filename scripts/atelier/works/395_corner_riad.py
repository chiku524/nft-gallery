"""Zellige crop. Independent salon work 395."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=395,
    slug='corner-riad',
    title='Corner Riad',
    description='A fragment of a courtyard.',
    medium='Zellige crop',
    motion='Crop',
    palette='Edge glaze',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (192, 29, 221), (63, 226, 34), (221, 161, 83), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts = [(256 + 180 * math.cos(k * math.tau / 8 + t * 0.1), 256 + 180 * math.sin(k * math.tau / 8 + t * 0.1)) for k in range(8)]
    draw.polygon([(int(x), int(y)) for x, y in pts], fill=ink, outline=accent, width=6)
    
    return canvas.convert("RGBA")
