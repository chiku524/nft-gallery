"""Mail crop. Independent salon work 449."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=449,
    slug='mail-crop',
    title='Mail Crop',
    description='A corner of a war.',
    medium='Mail crop',
    motion='Crop',
    palette='Edge steel',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (181, 61, 231), (74, 194, 24), (33, 184, 143), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    r = int(70 * scale)
    draw.ellipse((256 - r + ox, 256 - r + oy, 256 + r + ox, 256 + r + oy), outline=ink, width=14)
    draw.ellipse((256 - 12, 256 - 12, 256 + 12, 256 + 12), fill=accent)
    
    return canvas.convert("RGBA")
