"""Bird sgraffito. Independent salon work 301."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=301,
    slug='bird-scratch',
    title='Bird Scratch',
    description='A silhouette that is a scratch.',
    medium='Bird sgraffito',
    motion='Peck',
    palette='Avian slip',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (130, 192, 139), (12, 12, 14), (121, 139, 97), (71, 102, 76)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((60, 60, 452, 452), fill=ink)
    draw.arc((100, 100, 412, 412), 20 + t * 10, 200, fill=bg, width=12)
    
    return canvas.convert("RGBA")
