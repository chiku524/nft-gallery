"""Spike train. Independent salon work 411."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=411,
    slug='spikes',
    title='Spikes',
    description='A neuron with nowhere to live except this strip.',
    medium='Spike train',
    motion='Fire',
    palette='Night phosphor',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (33, 60, 235), (222, 195, 20), (148, 22, 189), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    pts = []
    for k in range(240):
        ang = k / 240 * math.tau + t * 0.2
        r = 40 + (160 * scale) + 26 * math.sin(k * 0.35 + t)
        pts.append((256 + ox + r * math.cos(ang), 256 + oy + r * math.sin(ang)))
    draw.line([(int(x), int(y)) for x, y in pts], fill=ink, width=3)
    
    return canvas.convert("RGBA")
