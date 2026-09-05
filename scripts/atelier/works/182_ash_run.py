"""Ash glaze. Independent salon work 182."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=182,
    slug='ash-run',
    title='Ash Run',
    description='The kiln’s weather, poured.',
    medium='Ash glaze',
    motion='Melt',
    palette='Wood ash',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (112, 154, 147), (12, 12, 14), (181, 184, 195), (62, 83, 80)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.pieslice((40, 40, 472, 472), 200, 20 + 20 * math.sin(t), fill=ink)
    draw.ellipse((220, 220, 300, 300), fill=accent)
    
    return canvas.convert("RGBA")
