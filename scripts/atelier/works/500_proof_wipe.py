"""Wiped proof. Independent salon work 500."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=500,
    slug='proof-wipe',
    title='Proof Wipe',
    description='The plate after the printer.',
    medium='Wiped proof',
    motion='Wipe',
    palette='Rag copper',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (247, 98, 73), (8, 157, 182), (223, 115, 95), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.ellipse((180, 180, 250, 250), fill=bg)
    draw.ellipse((280, 260, 350, 330), fill=accent)
    
    return canvas.convert("RGBA")
