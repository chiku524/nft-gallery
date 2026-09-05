"""Edge light. Independent salon work 348."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=348,
    slug='edge-lights',
    title='Edge Lights',
    description='Lights without a strip.',
    medium='Edge light',
    motion='Blink',
    palette='Blue edge',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (107, 14, 128), (148, 241, 127), (63, 239, 233), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line((80, 80, 432, 432), fill=ink, width=18)
    draw.line((120, 80, 472, 432), fill=accent, width=8)
    draw.line((200, 180, 312, 292), fill=bg, width=10)
    
    return canvas.convert("RGBA")
