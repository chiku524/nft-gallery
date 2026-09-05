"""Selvedge plaid. Independent salon work 475."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=475,
    slug='selvedge',
    title='Selvedge',
    description='The edge is the only honest part.',
    medium='Selvedge plaid',
    motion='Stop',
    palette='Mill cream',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (168, 89, 148), (12, 12, 14), (117, 234, 160), (90, 50, 81)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 30), (480, 256), (256, 482), (32, 256)], fill=ink)
    for i in range(-6, 7):
        draw.line((256 + i * 28, 30, 256 + i * 28, 482), fill=accent, width=2)
        draw.line((30, 256 + i * 28, 482, 256 + i * 28), fill=bg, width=2)
    
    return canvas.convert("RGBA")
