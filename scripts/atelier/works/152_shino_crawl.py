"""Shino. Independent salon work 152."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=152,
    slug='shino-crawl',
    title='Shino Crawl',
    description='The glaze refused to sit.',
    medium='Shino',
    motion='Crawl',
    palette='Shino orange',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (15, 194, 146), (240, 61, 109), (221, 57, 231), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 140), fill=ink)
    draw.polygon([(80, 140), (140, 420), (40, 420)], fill=accent)
    draw.polygon([(300, 140), (360, 460), (250, 460)], fill=mid)
    
    return canvas.convert("RGBA")
