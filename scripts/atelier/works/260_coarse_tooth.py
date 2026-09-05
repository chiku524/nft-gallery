"""Coarse rocker. Independent salon work 260."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=260,
    slug='coarse-tooth',
    title='Coarse Tooth',
    description='The rocker was sure.',
    medium='Coarse rocker',
    motion='Grit',
    palette='Heavy tooth',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (41, 92, 95), (214, 163, 160), (66, 129, 217), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.rectangle((0, 0, 512, 512), fill=ink)
    draw.ellipse((160 + ox, 140 + oy, 360, 360), fill=accent)
    
    return canvas.convert("RGBA")
