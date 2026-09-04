"""Urushi lacquer. Deep black, a red underlayer that breathes."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=39,
    slug="urushi",
    title="Urushi",
    description="Many coats of night. A red thought shows only when the light is wrong.",
    medium="Urushi",
    motion="Sheen",
    palette="Lacquer night",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    sheen = np.exp(-((xx - 220 - 40 * math.cos(t)) ** 2 + (yy - 180) ** 2) / 28000)
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    rgb[..., 0] = 12 + 90 * sheen
    rgb[..., 1] = 8 + 12 * sheen
    rgb[..., 2] = 10 + 10 * sheen
    rgb[..., 0] += 40 * np.exp(-((xx - 300) ** 2 + (yy - 340) ** 2) / 22000)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
