"""Dried deckle. Independent salon work 496."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=496,
    slug='dry-edge',
    title='Dry Edge',
    description='The tear, set.',
    medium='Dried deckle',
    motion='Cure',
    palette='Sun rag',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (157, 180, 196), (98, 75, 59), (29, 87, 118), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((90, 90, 300, 400), fill=mid, outline=ink)
    draw.rectangle((220, 140, 430, 440), fill=accent, outline=ink)
    
    return canvas.convert("RGBA")
