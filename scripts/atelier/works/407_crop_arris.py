"""Ogham crop. Independent salon work 407."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=407,
    slug='crop-arris',
    title='Crop Arris',
    description='A fragment of a name.',
    medium='Ogham crop',
    motion='Crop',
    palette='Edge stone',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (27, 77, 52), (228, 178, 203), (77, 108, 190), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((200, 60, 200, 450), fill=ink, width=8)
    draw.line((200, 180, 320, 140), fill=accent, width=6)
    draw.line((200, 260, 340, 260), fill=accent, width=6)
    
    return canvas.convert("RGBA")
