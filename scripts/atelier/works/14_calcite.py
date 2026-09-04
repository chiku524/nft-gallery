"""Polished stone. No object — only migrating veins."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=14,
    slug="calcite",
    title="Calcite",
    description="A slab of stone with nothing carved into it. The veins keep changing their mind.",
    medium="Polished stone",
    motion="Migrate",
    palette="Calcite ink",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    field = (
        np.sin((xx * 0.018) + np.sin(yy * 0.011 + t) * 3.2)
        + 0.55 * np.sin((xx * 0.041 + yy * 0.02) - t * 0.7)
        + 0.25 * np.sin((yy * 0.07) + t)
    )
    vein = np.exp(-8 * np.abs(field))
    stone = 228 + 12 * np.sin(xx * 0.04 + yy * 0.03)
    ink = 42 + 30 * np.sin(field * 2)
    tone = stone * (1.0 - vein) + ink * vein
    rust = np.clip(vein * 40, 0, 40)
    rgb = np.stack([tone + rust, tone * 0.97, tone * 0.93], axis=-1)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
