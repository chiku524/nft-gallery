"""Gold leaf. Independent salon work 75."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=75,
    slug='gold-leaf',
    title='Gold Leaf',
    description='A square of sun, thin as rumor.',
    medium='Gold leaf',
    motion='Lay',
    palette='Icon gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (165, 238, 174), (90, 17, 81), (237, 74, 167), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((60, 60, 452, 452), fill=ink)
    crack = int(40 * math.sin(t))
    draw.line((60, 200 + crack, 452, 280 - crack), fill=bg, width=3)
    draw.line((200, 60, 260, 452), fill=bg, width=2)
    
    return canvas.convert("RGBA")
