"""Single muqarnas. Independent salon work 163."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=163,
    slug='one-cell-vault',
    title='One Cell Vault',
    description='One stalactite.',
    medium='Single muqarnas',
    motion='Hang',
    palette='Lone gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (228, 193, 146), (27, 62, 109), (105, 81, 234), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256 + ox, 90 + oy), (360, 250), (150, 250)], fill=ink)
    
    return canvas.convert("RGBA")
