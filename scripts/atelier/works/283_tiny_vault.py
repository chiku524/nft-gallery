"""Miniature muqarnas. Independent salon work 283."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=283,
    slug='tiny-vault',
    title='Tiny Vault',
    description='A smaller heaven.',
    medium='Miniature muqarnas',
    motion='Glint',
    palette='Pocket gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (192, 233, 70), (63, 22, 185), (27, 188, 233), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.regular_polygon((256, 200, 80), 3, fill=ink)
    draw.regular_polygon((256, 320, 80), 3, rotation=180, fill=accent)
    
    return canvas.convert("RGBA")
