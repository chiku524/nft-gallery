"""Night print. Independent salon work 309."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=309,
    slug='night-pad',
    title='Night Pad',
    description='Pressed in the dark.',
    medium='Night print',
    motion='Press',
    palette='Void ink',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (190, 202, 124), (65, 53, 131), (74, 171, 106), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((90, 90, 300, 360), outline=ink, width=3)
    draw.ellipse((220, 140, 430, 400), outline=accent, width=3)
    
    return canvas.convert("RGBA")
