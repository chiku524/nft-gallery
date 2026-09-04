"""Infrared thermograph. Heat islands that migrate."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=50,
    slug="thermograph",
    title="Thermograph",
    description="A temperature with no body. The hot spots keep changing their address.",
    medium="Thermograph",
    motion="Migrate",
    palette="Infrared",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    heat = (
        np.exp(-((xx - 200 - 40 * math.cos(t)) ** 2 + (yy - 220) ** 2) / 18000)
        + 0.7 * np.exp(-((xx - 340) ** 2 + (yy - 300 - 30 * math.sin(t)) ** 2) / 14000)
        + 0.35 * np.exp(-((xx - 140) ** 2 + (yy - 380) ** 2) / 10000)
    )
    r = np.clip(20 + 420 * heat, 0, 255)
    g = np.clip(10 + 180 * np.sin(heat * math.pi), 0, 255)
    b = np.clip(80 - 80 * heat + 40 * (1 - heat), 0, 255)
    rgb = np.stack([r, g, b], axis=-1)
    return Image.fromarray(rgb.astype(np.uint8), "RGB").convert("RGBA")
