"""Deckle crop. Independent salon work 406."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=406,
    slug='edge-crop-rag',
    title='Edge Crop Rag',
    description='Only the tear.',
    medium='Deckle crop',
    motion='Crop',
    palette='Edge rag',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (248, 197, 140), (7, 58, 115), (82, 207, 39), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for x in range(40, 480, 18):
        draw.line((x, 40, x, 472), fill=ink, width=1)
    for x in range(40, 480, 72):
        draw.line((x, 40, x, 472), fill=accent, width=3)
    
    return canvas.convert("RGBA")
