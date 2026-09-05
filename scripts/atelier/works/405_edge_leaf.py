"""Leaf crop. Independent salon work 405."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=405,
    slug='edge-leaf',
    title='Edge Leaf',
    description='A fragment of an icon.',
    medium='Leaf crop',
    motion='Crop',
    palette='Edge gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (59, 223, 239), (196, 32, 16), (49, 135, 131), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((90, 90, 422, 422), fill=accent)
    draw.rectangle((140, 140, 372, 372), fill=ink)
    
    return canvas.convert("RGBA")
