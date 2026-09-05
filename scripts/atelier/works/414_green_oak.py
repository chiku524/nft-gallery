"""Green oak. Independent salon work 414."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=414,
    slug='green-oak',
    title='Green Oak',
    description='Unseasoned and already a pattern.',
    medium='Green oak',
    motion='Cure',
    palette='Raw sap',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (152, 117, 150), (12, 12, 14), (102, 95, 198), (82, 64, 82)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 60), (452, 256), (256, 452), (60, 256)], outline=ink, width=6)
    for i in range(8):
        r = 40 + i * 22
        draw.rectangle((256 - r, 256 - 8, 256 + r, 256 + 8), outline=accent)
        draw.rectangle((256 - 8, 256 - r, 256 + 8, 256 + r), outline=ink)
    
    return canvas.convert("RGBA")
