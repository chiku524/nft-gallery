"""Drip stamp. Independent salon work 482."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=482,
    slug='postage-drip',
    title='Postage Drip',
    description='A shard, issued.',
    medium='Drip stamp',
    motion='Crop',
    palette='Shard green',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (238, 45, 70), (17, 210, 185), (71, 53, 137), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.pieslice((40, 40, 472, 472), 200, 20 + 20 * math.sin(t), fill=ink)
    draw.ellipse((220, 220, 300, 300), fill=accent)
    
    return canvas.convert("RGBA")
