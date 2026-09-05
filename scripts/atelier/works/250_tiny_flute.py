"""Microflute. Independent salon work 250."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=250,
    slug='tiny-flute',
    title='Tiny Flute',
    description='A smaller box.',
    medium='Microflute',
    motion='Tick',
    palette='Mailer kraft',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (83, 155, 241), (172, 100, 14), (27, 156, 159), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts_a, pts_b = [], []
    for y in range(0, 512, 4):
        wave = int(16 * scale * math.sin(y * 0.08 + t))
        pts_a.append((180 + wave, y))
        pts_b.append((320 + wave, y))
    draw.line(pts_a, fill=ink, width=10)
    draw.line(pts_b, fill=accent, width=10)
    
    return canvas.convert("RGBA")
