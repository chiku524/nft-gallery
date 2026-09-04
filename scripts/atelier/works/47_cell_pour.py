"""Paint pour cells. Hard cellular skins, not a soft wash."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=47,
    slug="cell-pour",
    title="Cell Pour",
    description="Acrylic that decided to become a map. The cells breathe without blending.",
    medium="Paint pour",
    motion="Cell",
    palette="Pour jewel",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    seeds = np.array(
        [
            [140 + 20 * math.sin(t), 160],
            [320, 140 + 18 * math.cos(t)],
            [250, 300],
            [400, 340],
            [120, 380],
            [360, 240],
        ]
    )
    colors = np.array(
        [
            [196, 48, 72],
            [28, 92, 148],
            [214, 176, 48],
            [48, 128, 96],
            [148, 64, 140],
            [236, 120, 64],
        ],
        dtype=np.float32,
    )
    dist = np.stack([np.sqrt((xx - sx) ** 2 + (yy - sy) ** 2) for sx, sy in seeds], axis=0)
    nearest = dist.argmin(axis=0)
    rgb = colors[nearest]
    edge = np.sort(dist, axis=0)[1] - np.sort(dist, axis=0)[0]
    rgb = np.where(edge[..., None] < 4, rgb * 0.35, rgb)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
