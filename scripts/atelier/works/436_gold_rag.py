"""Gilt deckle. Independent salon work 436."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=436,
    slug='gold-rag',
    title='Gold Rag',
    description='A torn edge dressed up.',
    medium='Gilt deckle',
    motion='Flash',
    palette='Luxury rag',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (207, 119, 30), (48, 136, 225), (226, 52, 96), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((70, 70, 442, 442), fill=mid)
    draw.ellipse((180, 180, 332, 332), outline=ink, width=1)
    
    return canvas.convert("RGBA")
