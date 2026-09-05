"""Worn runway. Independent salon work 288."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=288,
    slug='worn-paint',
    title='Worn Paint',
    description='The landing wore the law away.',
    medium='Worn runway',
    motion='Fade',
    palette='Traffic yellow',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (207, 77, 236), (48, 178, 19), (117, 120, 48), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 40), (300, 120), (212, 120)], fill=ink)
    draw.polygon([(256, 472), (300, 392), (212, 392)], fill=ink)
    draw.rectangle((248, 140, 264, 372), fill=accent)
    
    return canvas.convert("RGBA")
