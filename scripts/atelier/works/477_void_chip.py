"""Missing chip. Independent salon work 477."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=477,
    slug='void-chip',
    title='Void Chip',
    description='The stone that left.',
    medium='Missing chip',
    motion='Gap',
    palette='Hole mint',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (14, 211, 192), (241, 44, 63), (143, 230, 210), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(40, 40), (472, 90), (430, 470), (70, 440)], fill=mid)
    draw.polygon([(200, 180), (260, 160), (240, 230)], fill=accent)
    draw.polygon([(300, 300), (360, 280), (340, 350)], fill=ink)
    
    return canvas.convert("RGBA")
