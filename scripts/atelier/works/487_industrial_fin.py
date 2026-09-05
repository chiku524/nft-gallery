"""Cooling fin. Independent salon work 487."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=487,
    slug='industrial-fin',
    title='Industrial Fin',
    description='A blind that thinks it is an engine.',
    medium='Cooling fin',
    motion='Radiate',
    palette='Machine slat',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (110, 62, 51), (145, 193, 204), (92, 111, 184), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 200, 472, 280), fill=ink)
    draw.rectangle((40, 200, 472, 220), fill=accent)
    
    return canvas.convert("RGBA")
