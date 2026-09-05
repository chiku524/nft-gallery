"""Single drip. Independent salon work 332."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=332,
    slug='drip-only',
    title='Drip Only',
    description='One decision, gravity’s.',
    medium='Single drip',
    motion='Drop',
    palette='Lone glaze',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (86, 161, 14), (169, 94, 241), (29, 217, 31), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.pieslice((40, 40, 472, 472), 200, 20 + 20 * math.sin(t), fill=ink)
    draw.ellipse((220, 220, 300, 300), fill=accent)
    
    return canvas.convert("RGBA")
