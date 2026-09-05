"""Broken muqarnas. Independent salon work 313."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=313,
    slug='broken-cell',
    title='Broken Cell',
    description='The cave failed.',
    medium='Broken muqarnas',
    motion='Gap',
    palette='Ruin gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (158, 188, 102), (97, 67, 153), (216, 30, 202), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256 + ox, 90 + oy), (360, 250), (150, 250)], fill=ink)
    
    return canvas.convert("RGBA")
