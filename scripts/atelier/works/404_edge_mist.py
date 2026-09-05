"""Stencil crop. Independent salon work 404."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=404,
    slug='edge-mist',
    title='Edge Mist',
    description='A fragment of an order.',
    medium='Stencil crop',
    motion='Crop',
    palette='Edge spray',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (57, 151, 118), (244, 240, 232), (215, 188, 100), (150, 195, 175)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((80, 80, 200, 400), fill=ink)
    draw.rectangle((140, 140, 180, 200), fill=bg)
    draw.rectangle((140, 240, 180, 340), fill=bg)
    
    return canvas.convert("RGBA")
