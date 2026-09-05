"""Ogham edge. Independent salon work 137."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=137,
    slug='edge-script',
    title='Edge Script',
    description='The arris is the page.',
    medium='Ogham edge',
    motion='Climb',
    palette='Pillar grey',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (85, 213, 13), (170, 42, 242), (148, 42, 37), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for x in (160, 256, 352):
        draw.line((x, 50, x, 460), fill=ink, width=5)
        for i in range(8):
            y = 70 + i * 48
            draw.line((x - 30, y, x + 30, y - 12), fill=accent, width=3)
    
    return canvas.convert("RGBA")
