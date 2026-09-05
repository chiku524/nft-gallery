"""Miniature print. Independent salon work 369."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=369,
    slug='tiny-whorl',
    title='Tiny Whorl',
    description='A smaller someone.',
    medium='Miniature print',
    motion='Spin',
    palette='Pocket ink',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (219, 196, 117), (36, 59, 138), (176, 52, 183), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    for ring in range(10, int(180 * scale), 8):
        draw.ellipse((256 - ring + ox, 256 - ring + oy, 256 + ring + ox, 256 + ring + oy), outline=ink, width=2)
    
    return canvas.convert("RGBA")
