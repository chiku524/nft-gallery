"""Miniature deckle. Independent salon work 316."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=316,
    slug='tiny-sheet',
    title='Tiny Sheet',
    description='A smaller sheet.',
    medium='Miniature deckle',
    motion='Crop',
    palette='Pocket rag',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (164, 37, 216), (91, 218, 39), (30, 179, 75), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(40, 80), (470, 60), (450, 450), (70, 430)], fill=mid, outline=ink)
    
    return canvas.convert("RGBA")
