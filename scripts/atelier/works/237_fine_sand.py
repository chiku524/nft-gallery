"""Fine terrazzo. Independent salon work 237."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=237,
    slug='fine-sand',
    title='Fine Sand',
    description='Almost a color field. Then a stone speaks.',
    medium='Fine terrazzo',
    motion='Dust',
    palette='Pale grit',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (131, 25, 151), (124, 230, 104), (66, 222, 121), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((40, 40, 472, 40), fill=accent, width=8)
    draw.line((40, 40, 40, 472), fill=accent, width=8)
    rng = np.random.default_rng(8)
    for n in range(50):
        x, y = int(rng.integers(60, 450)), int(rng.integers(60, 450))
        draw.ellipse((x, y, x + 16, y + 10), fill=ink if n % 2 else mid)
    
    return canvas.convert("RGBA")
