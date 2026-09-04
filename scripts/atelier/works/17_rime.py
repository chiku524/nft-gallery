"""Window frost. Dendrites grow from one corner, then hold."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=17,
    slug="rime",
    title="Rime",
    description="Ice writes a tree on cold glass. The growth is the drawing.",
    medium="Frost",
    motion="Grow",
    palette="Ice pane",
)


def paint(frame: int) -> Image.Image:
    t = (frame + 1) / 12
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    pane = 18 + 10 * (yy / SIZE)
    rgb = np.stack([pane * 0.7, pane * 0.85, pane + 16], axis=-1)
    rng = np.random.default_rng(17)
    tips = [(36, 478), (80, 500), (20, 430)]
    for step in range(int(900 * t) + 80):
        x, y = tips[step % len(tips)]
        angle = rng.uniform(-1.1, 0.2) - 1.15
        nx = int(np.clip(x + 6 * math.cos(angle), 6, 505))
        ny = int(np.clip(y + 6 * math.sin(angle), 6, 505))
        for ox in range(-2, 3):
            for oy in range(-2, 3):
                if abs(ox) + abs(oy) <= 3:
                    rgb[ny + oy, nx + ox] = (214, 230, 246)
        if step % 5 == 0:
            tips.append((nx, ny))
        else:
            tips[step % len(tips)] = (nx, ny)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
