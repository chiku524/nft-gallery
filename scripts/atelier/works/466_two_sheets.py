"""Overlapped deckle. Independent salon work 466."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=466,
    slug='two-sheets',
    title='Two Sheets',
    description='Two tears conferring.',
    medium='Overlapped deckle',
    motion='Stack',
    palette='Twin rag',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (201, 135, 221), (54, 120, 34), (39, 164, 212), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(40, 80), (470, 60), (450, 450), (70, 430)], fill=mid, outline=ink)
    
    return canvas.convert("RGBA")
