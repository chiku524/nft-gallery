"""Paillette. Independent salon work 173."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=173,
    slug='paillette',
    title='Paillette',
    description='Costume armor for a room.',
    medium='Paillette',
    motion='Flicker',
    palette='Show gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (88, 137, 197), (167, 118, 58), (147, 113, 68), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((60, 80, 450, 470), outline=ink, width=8)
    for y in range(120, 420, int(36 * scale)):
        for x in range(100, 400, 40):
            draw.chord((x, y, x + 34, y + 24), 210, 330, fill=accent)
    
    return canvas.convert("RGBA")
