"""Chalk on slate. White dust that writes and forgets."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=44,
    slug="slate-dust",
    title="Slate Dust",
    description="A blackboard with no lesson. The dust keeps a stroke that will not stay.",
    medium="Chalk",
    motion="Dust",
    palette="Slate white",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (28, 34, 40))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((24, 24, 488, 488), outline=(18, 18, 18), width=10)
    rng = np.random.default_rng(44 + frame)
    for _ in range(180):
        x = int(rng.integers(50, 460))
        y = int(rng.integers(50, 460))
        draw.point((x, y), fill=(220, 220, 214))
    x0, y0 = 80, 360
    x1 = 80 + int(300 * (0.5 + 0.5 * math.sin(t)))
    y1 = 360 - int(160 * (0.5 + 0.5 * math.sin(t)))
    draw.line((x0, y0, x1, y1), fill=(230, 230, 224), width=6)
    return canvas.convert("RGBA")
