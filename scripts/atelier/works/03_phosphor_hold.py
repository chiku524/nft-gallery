"""CRT phosphor. Scanlines, a held reticle, raster roll."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=3,
    slug="phosphor-hold",
    title="Phosphor Hold",
    description="A green reticle waits on a dead monitor. The raster still believes in work.",
    medium="CRT phosphor",
    motion="Raster roll",
    palette="Phosphor black",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    roll = (yy + frame * 7) % 3
    scan = np.where(roll == 0, 0.55, 1.0)
    cx, cy = 256.0, 248.0
    reticle = np.exp(-0.5 * (((xx - cx) / 86) ** 2 + ((yy - cy) / 64) ** 2))
    ring = np.abs(np.sqrt((xx - cx) ** 2 + ((yy - cy) * 1.15) ** 2) - 92)
    ring = np.clip(1.0 - ring / 2.4, 0, 1)
    cross = ((np.abs(xx - cx) < 1.2) & (np.abs(yy - cy) < 70)) | (
        (np.abs(yy - cy) < 1.2) & (np.abs(xx - cx) < 90)
    )
    pulse = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t * 2))
    green = 18 + 210 * (reticle * 0.35 + ring * pulse) * scan
    green = np.where(cross, np.maximum(green, 200 * pulse), green)
    vig = 1.0 - 0.45 * (((xx - 256) / 360) ** 2 + ((yy - 256) / 360) ** 2)
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    rgb[..., 1] = np.clip(green * vig, 0, 255)
    rgb[..., 0] = rgb[..., 1] * 0.18
    rgb[..., 2] = rgb[..., 1] * 0.22
    return Image.fromarray(rgb.astype(np.uint8), "RGB").convert("RGBA")
