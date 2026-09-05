"""Deckle. Independent salon work 76."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=76,
    slug='deckle-edge',
    title='Deckle Edge',
    description='The edge that refuses a guillotine.',
    medium='Deckle',
    motion='Tear',
    palette='Rag cream',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (107, 158, 238), (148, 97, 17), (64, 222, 133), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
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
