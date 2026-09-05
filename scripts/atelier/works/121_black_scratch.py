"""Black sgraffito. Independent salon work 121."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=121,
    slug='black-scratch',
    title='Black Scratch',
    description='The line is a wound in soot.',
    medium='Black sgraffito',
    motion='Cut',
    palette='Night slip',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (137, 57, 172), (118, 198, 83), (180, 201, 111), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((40, 40, 472, 472), fill=ink)
    for y in range(70, 450, int(28 * scale)):
        draw.line((70, y, 440, y + int(20 * math.sin(t + y))), fill=bg, width=2)
    
    return canvas.convert("RGBA")
