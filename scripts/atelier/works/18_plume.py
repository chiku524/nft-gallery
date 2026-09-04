"""Ink in water. Soft plumes, no contour, a rise that never thins to a line."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=18,
    slug="plume",
    title="Plume",
    description="Pigment forgets it had an edge. The rise is slower than smoke and thicker than air.",
    medium="Ink in water",
    motion="Rise",
    palette="Indigo milk",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    paper = np.array([236, 228, 214], dtype=np.float32)
    ink_a = np.array([36, 28, 78], dtype=np.float32)
    ink_b = np.array([148, 64, 72], dtype=np.float32)
    lift = 28 * math.sin(t)
    a = np.exp(-((xx - 220) ** 2 / 14000 + (yy - 340 + lift) ** 2 / 28000))
    a += 0.65 * np.exp(-((xx - 300 + 20 * math.cos(t)) ** 2 / 9000 + (yy - 260) ** 2 / 22000))
    b = np.exp(-((xx - 280) ** 2 / 18000 + (yy - 200 - lift) ** 2 / 16000))
    rgb = paper * (1 - a[..., None] * 0.85) + ink_a * (a[..., None] * 0.85)
    rgb = rgb * (1 - b[..., None] * 0.55) + ink_b * (b[..., None] * 0.55)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
