"""Crawl white. Independent salon work 392."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=392,
    slug='white-crawl',
    title='White Crawl',
    description='The white left islands.',
    medium='Crawl white',
    motion='Shrink',
    palette='Snow crawl',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (82, 118, 32), (173, 137, 223), (120, 94, 205), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((90, 90, 422, 422), fill=ink)
    draw.ellipse((180, 170, 300, 290), fill=accent)
    
    return canvas.convert("RGBA")
