"""Torn rag. Independent salon work 196."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=196,
    slug='torn-sheet',
    title='Torn Sheet',
    description='A sheet that chose its own border.',
    medium='Torn rag',
    motion='Rip',
    palette='Rag wound',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (139, 113, 47), (244, 240, 232), (181, 187, 112), (191, 176, 139)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((90, 90, 300, 400), fill=mid, outline=ink)
    draw.rectangle((220, 140, 430, 440), fill=accent, outline=ink)
    
    return canvas.convert("RGBA")
