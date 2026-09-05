"""Gilt scale. Independent salon work 443."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=443,
    slug='gilt-scale',
    title='Gilt Scale',
    description='A relic that repeats itself.',
    medium='Gilt scale',
    motion='Burnish',
    palette='Icon gold',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (152, 183, 180), (103, 72, 75), (198, 235, 228), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 70), (420, 400), (90, 400)], fill=mid)
    for i, (x, y) in enumerate(((200, 180), (280, 200), (230, 260), (300, 280), (180, 300))):
        draw.chord((x, y, x + 50, y + 36), 200, 340, fill=accent if i == frame % 5 else ink)
    
    return canvas.convert("RGBA")
