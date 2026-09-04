"""Copper etching. Green plate, circular bites that deepen."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=34,
    slug="bitten-plate",
    title="Bitten Plate",
    description="Acid remembers every circle. The plate darkens where the bite holds.",
    medium="Etching",
    motion="Bite",
    palette="Verdigris copper",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    plate = np.stack(
        [
            np.full((SIZE, SIZE), 48 + 20 * np.sin(xx * 0.01)),
            np.full((SIZE, SIZE), 86 + 16 * np.cos(yy * 0.012)),
            np.full((SIZE, SIZE), 64),
        ],
        axis=-1,
    )
    depth = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t))
    for i, (cx, cy, r) in enumerate(((180, 190, 70), (320, 250, 90), (240, 340, 50), (360, 160, 40))):
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        ring = np.exp(-((d - r) ** 2) / 18)
        plate[..., 0] -= ring * 20 * depth
        plate[..., 1] -= ring * 10 * depth
        plate[..., 2] -= ring * 8 * depth
    return Image.fromarray(np.clip(plate, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
