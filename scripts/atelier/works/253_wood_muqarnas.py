"""Wood muqarnas. Independent salon work 253."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=253,
    slug='wood-muqarnas',
    title='Wood Muqarnas',
    description='Carpentry pretending it is stone.',
    medium='Wood muqarnas',
    motion='Join',
    palette='Cedar vault',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (15, 96, 206), (240, 159, 49), (66, 24, 239), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 80), (400, 220), (330, 400), (180, 400), (110, 220)], fill=mid, outline=ink, width=6)
    draw.polygon([(256, 160), (320, 240), (256, 300), (190, 240)], fill=accent)
    
    return canvas.convert("RGBA")
