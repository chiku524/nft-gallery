"""Fire cloisonné. Independent salon work 480."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=480,
    slug='fire-scale',
    title='Fire Scale',
    description='The firing left a weather of its own.',
    medium='Fire cloisonné',
    motion='Pit',
    palette='Kiln ash',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (40, 183, 15), (215, 72, 240), (81, 240, 33), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.polygon([(256, 60), (430, 200), (370, 430), (140, 430), (80, 200)], fill=mid, outline=ink, width=8)
    draw.ellipse((200, 190, 312, 300), fill=accent)
    
    return canvas.convert("RGBA")
