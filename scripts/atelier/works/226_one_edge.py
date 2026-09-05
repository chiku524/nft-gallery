"""Single deckle. Independent salon work 226."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=226,
    slug='one-edge',
    title='One Edge',
    description='One ragged decision.',
    medium='Single deckle',
    motion='Hold',
    palette='Lone rag',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (52, 204, 131), (203, 51, 124), (132, 198, 117), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    rng = np.random.default_rng(4)
    pts = []
    for i in range(40):
        ang = i / 40 * math.tau
        r = 200 + int(rng.integers(-18, 18))
        pts.append((256 + r * math.cos(ang), 256 + r * math.sin(ang)))
    draw.polygon([(int(x), int(y)) for x, y in pts], fill=mid, outline=ink)
    
    return canvas.convert("RGBA")
