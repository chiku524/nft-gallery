"""Teak deck. Independent salon work 204."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=204,
    slug='ship-deck',
    title='Ship Deck',
    description='A boat that will not leave the salon.',
    medium='Teak deck',
    motion='Caulk',
    palette='Marine teak',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (178, 114, 142), (12, 12, 14), (236, 228, 131), (95, 63, 78)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    w, h = int(70 * scale), int(18 * scale)
    for row in range(16):
        for col in range(10):
            x = 20 + col * (w + 4) + (row % 2) * w // 2
            y = 20 + row * (h + 6)
            tilt = 18 if (row + col) % 2 == 0 else -18
            draw.polygon([(x, y), (x + w, y + tilt), (x + w, y + h + tilt), (x, y + h)], fill=ink if (row + col + frame) % 4 else accent)
    
    return canvas.convert("RGBA")
