"""Tartan sett. Independent salon work 55."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=55,
    slug='clan-sett',
    title='Clan Sett',
    description='A family reduced to crossings.',
    medium='Tartan sett',
    motion='Lock',
    palette='Wool night',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (73, 14, 109), (182, 241, 146), (109, 77, 177), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for x in range(0, 512, int(28 * scale)):
        draw.rectangle((x, 0, x + 10, 512), fill=ink)
    for y in range(0, 512, int(36 * scale)):
        draw.rectangle((0, y, 512, y + 8), fill=accent)
    draw.rectangle((0, 0, 512, 512), outline=mid, width=18)
    
    return canvas.convert("RGBA")
