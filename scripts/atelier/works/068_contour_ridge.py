"""Topographic ink. Independent salon work 68."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=68,
    slug='contour-ridge',
    title='Contour Ridge',
    description='Height without a hill.',
    medium='Topographic ink',
    motion='Wind',
    palette='Survey brown',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (214, 240, 156), (41, 15, 99), (189, 78, 82), (127, 127, 127)
    scale, ox, oy, spin = 0.720, -70, 60, 0.000
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    z = np.sin((xx - 256 - ox) * 0.02 * scale) + np.cos((yy - 256 - oy) * 0.02 * scale + t)
    rings = np.sin(z * 6)
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    for c in range(3):
        rgb[..., c] = bg[c] + (ink[c] - bg[c]) * (rings > 0)
    canvas = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")
    draw = ImageDraw.Draw(canvas)
    
    return canvas.convert("RGBA")
