"""Weather radar. A green sweep that finds nothing twice."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=40,
    slug="radar-sweep",
    title="Radar Sweep",
    description="A scope that keeps a storm that is not there. The arm is the weather.",
    medium="Radar",
    motion="Sweep",
    palette="Scope green",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    ang = np.arctan2(yy - 256, xx - 256)
    d = np.sqrt((xx - 256) ** 2 + (yy - 256) ** 2)
    sweep = np.clip(1.0 - np.abs(((ang - t + math.pi) % math.tau) - math.pi) * 2.2, 0, 1)
    rings = np.exp(-((d % 70 - 2) ** 2) / 8) * 0.35
    echo = np.exp(-((xx - 340) ** 2 + (yy - 200) ** 2) / 4000) * (0.4 + 0.4 * math.sin(t))
    green = 8 + 210 * sweep * np.clip(1.0 - d / 250, 0, 1) + 80 * rings + 180 * echo
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    rgb[..., 1] = np.clip(green, 0, 255)
    rgb[..., 0] = rgb[..., 1] * 0.15
    return Image.fromarray(rgb.astype(np.uint8), "RGB").convert("RGBA")
