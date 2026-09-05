"""Prepared piano. Independent salon work 123."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=123,
    slug='prepared',
    title='Prepared',
    description='Objects on strings you cannot see.',
    medium='Prepared piano',
    motion='Mute',
    palette='Felt brass',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (66, 64, 143), (189, 191, 112), (220, 45, 52), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((60, 180, 452, 260), fill=ink)
    draw.rectangle((200 + int(40 * math.sin(t)), 160, 280 + int(40 * math.sin(t)), 280), fill=accent)
    
    return canvas.convert("RGBA")
