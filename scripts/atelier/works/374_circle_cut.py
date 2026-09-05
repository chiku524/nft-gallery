"""Circle stencil. Independent salon work 374."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=374,
    slug='circle-cut',
    title='Circle Cut',
    description='A hole that makes a moon.',
    medium='Circle stencil',
    motion='Cut',
    palette='Dot spray',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (215, 236, 60), (40, 19, 195), (35, 57, 240), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.regular_polygon((256 + ox, 256 + oy, int(140 * scale)), 5, rotation=t * 6, fill=ink)
    draw.regular_polygon((256 + ox, 256 + oy, 50), 5, rotation=t * 6, fill=bg)
    
    return canvas.convert("RGBA")
