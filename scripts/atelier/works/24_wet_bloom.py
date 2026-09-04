"""Wet-in-wet watercolor. Soft blooms, paper tooth, one stain that expands."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=24,
    slug="wet-bloom",
    title="Wet Bloom",
    description="Water gets there first. Pigment follows and refuses a border.",
    medium="Watercolor",
    motion="Expand",
    palette="Wash coral",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    paper = np.array([244, 236, 222], dtype=np.float32)
    tooth = ((xx * 12.9898 + yy * 78.233) % 1.0) * 8 - 4
    grow = 1.0 + 0.18 * math.sin(t)
    stain = np.exp(-((xx - 210) ** 2 + (yy - 240) ** 2) / (21000 * grow))
    stain += 0.7 * np.exp(-((xx - 320) ** 2 + (yy - 300) ** 2) / (16000 * grow))
    edge = np.clip(stain * 1.4, 0, 1)
    coral = np.array([196, 86, 72], dtype=np.float32)
    sap = np.array([64, 110, 92], dtype=np.float32)
    rgb = paper + tooth[..., None]
    rgb = rgb * (1 - edge[..., None] * 0.72) + coral * (edge[..., None] * 0.72)
    second = np.exp(-((xx - 300) ** 2 + (yy - 180) ** 2) / 12000)
    rgb = rgb * (1 - second[..., None] * 0.4) + sap * (second[..., None] * 0.4)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
