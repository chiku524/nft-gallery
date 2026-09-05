"""Corrugate crop. Independent salon work 400."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=400,
    slug='edge-crop',
    title='Edge Crop',
    description='The cut is the picture.',
    medium='Corrugate crop',
    motion='Crop',
    palette='Cut kraft',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (148, 203, 70), (107, 52, 185), (100, 91, 182), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
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
