"""Scale stamp. Independent salon work 473."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=473,
    slug='postage-scale',
    title='Postage Scale',
    description='Armor, perforated.',
    medium='Scale stamp',
    motion='Crop',
    palette='Issue blue',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (51, 82, 82), (204, 173, 173), (186, 146, 194), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((60, 80, 450, 470), outline=ink, width=8)
    for y in range(120, 420, int(36 * scale)):
        for x in range(100, 400, 40):
            draw.chord((x, y, x + 34, y + 24), 210, 330, fill=accent)
    
    return canvas.convert("RGBA")
