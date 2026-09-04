"""Op-art interference. Two ring fields, a moiré that walks."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=8,
    slug="interference",
    title="Interference",
    description="Two ring families argue in black and white. The moiré is the only subject.",
    medium="Op-art",
    motion="Phase",
    palette="Ink paper",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    a = np.sqrt((xx - 220) ** 2 + (yy - 256) ** 2)
    b = np.sqrt((xx - 300 + 18 * math.cos(t)) ** 2 + (yy - 248) ** 2)
    rings = np.sin(a * 0.28 + t) * np.sin(b * 0.31 - t * 1.1)
    ink = np.where(rings > 0, 18, 242)
    rgb = np.stack([ink, ink, ink], axis=-1)
    return Image.fromarray(rgb.astype(np.uint8), "RGB").convert("RGBA")
