"""Hammer felt. Independent salon work 303."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=303,
    slug='felt-hammer',
    title='Felt Hammer',
    description='The hit, without the string.',
    medium='Hammer felt',
    motion='Strike',
    palette='Felt dust',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (181, 69, 103), (74, 186, 152), (161, 221, 20), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((80, 200, 432, 280), fill=mid, outline=ink, width=6)
    draw.ellipse((220, 210, 300, 270), fill=accent)
    
    return canvas.convert("RGBA")
