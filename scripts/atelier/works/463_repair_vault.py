"""Repaired muqarnas. Independent salon work 463."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=463,
    slug='repair-vault',
    title='Repair Vault',
    description='The new cell does not match.',
    medium='Repaired muqarnas',
    motion='Patch',
    palette='Misfit gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (56, 25, 22), (199, 230, 233), (49, 56, 227), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256 + ox, 90 + oy), (360, 250), (150, 250)], fill=ink)
    
    return canvas.convert("RGBA")
