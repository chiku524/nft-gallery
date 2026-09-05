"""Single centerline. Independent salon work 228."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=228,
    slug='one-stripe',
    title='One Stripe',
    description='One decision about direction.',
    medium='Single centerline',
    motion='Hold',
    palette='Lone yellow',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (198, 244, 193), (57, 11, 62), (98, 166, 32), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((220, 20, 292, 492), fill=mid)
    for y in range(30, 480, 36):
        draw.rectangle((246, y, 266, y + 18), fill=ink if (y // 36 + frame) % 2 else accent)
    
    return canvas.convert("RGBA")
