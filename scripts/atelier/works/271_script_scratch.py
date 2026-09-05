"""Script sgraffito. Independent salon work 271."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=271,
    slug='script-scratch',
    title='Script Scratch',
    description='Words that are only their absence.',
    medium='Script sgraffito',
    motion='Write',
    palette='Letter slip',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (122, 172, 57), (133, 83, 198), (93, 137, 79), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 40, 472, 472), fill=ink)
    for y in range(70, 450, int(28 * scale)):
        draw.line((70, y, 440, y + int(20 * math.sin(t + y))), fill=bg, width=2)
    
    return canvas.convert("RGBA")
