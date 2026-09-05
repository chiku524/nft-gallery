"""Salt glaze. Independent salon work 242."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=242,
    slug='salt-orange',
    title='Salt Orange',
    description='Orange-peel from a vapor.',
    medium='Salt glaze',
    motion='Pit',
    palette='Salt orange',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (195, 248, 127), (60, 7, 128), (132, 121, 230), (127, 127, 127)
    scale, ox, oy, spin = 1.000, 0, 0, 0.350
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.ellipse((90, 90, 422, 422), fill=ink)
    draw.ellipse((180, 170, 300, 290), fill=accent)
    
    return canvas.convert("RGBA")
