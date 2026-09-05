"""Night tenmoku. Independent salon work 452."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=452,
    slug='night-tenmoku',
    title='Night Tenmoku',
    description='Blacker than the room.',
    medium='Night tenmoku',
    motion='Pool',
    palette='Void iron',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (243, 178, 227), (12, 77, 28), (38, 210, 133), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 140), fill=ink)
    draw.polygon([(80, 140), (140, 420), (40, 420)], fill=accent)
    draw.polygon([(300, 140), (360, 460), (250, 460)], fill=mid)
    
    return canvas.convert("RGBA")
