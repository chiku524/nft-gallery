"""Encaustic wax. Thick slabs, an embedded color that wells."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=45,
    slug="encaustic",
    title="Encaustic",
    description="Wax poured over a thought. The thought keeps trying to surface.",
    medium="Encaustic",
    motion="Well",
    palette="Wax umber",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    wax = np.array([214, 186, 140], dtype=np.float32)
    umber = np.array([92, 56, 32], dtype=np.float32)
    well = np.exp(-((xx - 260) ** 2 + (yy - 240 - 16 * math.sin(t)) ** 2) / 18000)
    ridge = 8 * np.sin(xx * 0.08 + np.sin(yy * 0.03))
    rgb = wax + ridge[..., None] + (umber - wax) * well[..., None] * (0.55 + 0.25 * math.sin(t))
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
