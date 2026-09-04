"""Risograph. Two ink plates, multiply overprint, registration drift."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=2,
    slug="two-plate",
    title="Two Plate Offset",
    description="Fluorescent pink and teal miss each other on purpose. The overlap is the print.",
    medium="Risograph",
    motion="Misregister",
    palette="Pink teal pulp",
)


def _plate(cx: float, cy: float, rx: float, ry: float, rot: float) -> np.ndarray:
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    ca, sa = math.cos(rot), math.sin(rot)
    x = (xx - cx) * ca + (yy - cy) * sa
    y = -(xx - cx) * sa + (yy - cy) * ca
    return np.clip(1.0 - ((x / rx) ** 2 + (y / ry) ** 2), 0.0, 1.0) ** 0.55


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    paper = np.array([246, 238, 214], dtype=np.float32)
    pink = np.array([255, 46, 136], dtype=np.float32)
    teal = np.array([12, 168, 164], dtype=np.float32)
    dx = 10 * math.sin(t)
    dy = 7 * math.cos(t * 0.8)
    a = _plate(250 + dx, 250 + dy, 168, 210, 0.22 + 0.04 * math.sin(t))
    b = _plate(300 - dx, 280 - dy, 190, 150, -0.35)
    rgb = paper[None, None, :] * np.ones((SIZE, SIZE, 3), dtype=np.float32)
    rgb = rgb * (1.0 - a[..., None] * 0.78) + pink * (a[..., None] * 0.78)
    over = b[..., None] * 0.72
    rgb = rgb * (1.0 - over) + (rgb * (teal / 255.0) * 255.0) * over
    grain = (np.random.default_rng(frame + 9).random((SIZE, SIZE, 1)) - 0.5) * 10
    rgb = np.clip(rgb + grain, 0, 255)
    return Image.fromarray(rgb.astype(np.uint8), "RGB").convert("RGBA")
