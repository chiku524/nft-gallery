"""Night photograph. Almost nothing but grain and a held horizon."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=9,
    slug="hold-still",
    title="Hold Still",
    description="A night that refuses a subject. The grain is the only thing that moves.",
    medium="Silver grain",
    motion="Crawl",
    palette="Night silver",
)


def paint(frame: int) -> Image.Image:
    rng = np.random.default_rng(4400 + frame * 17)
    grain = rng.normal(0, 18, (SIZE, SIZE)).astype(np.float32)
    yy = np.linspace(0, 1, SIZE, dtype=np.float32)[:, None]
    sky = 18 + 22 * (1.0 - yy)
    land = 8 + 6 * yy
    horizon = 1.0 / (1.0 + np.exp((yy - 0.62) * 40))
    base = sky * horizon + land * (1.0 - horizon)
    pulse = 4 * math.sin(frame / 12 * math.tau)
    tone = np.clip(base + grain + pulse * horizon, 0, 255)
    rgb = np.stack([tone * 0.92, tone * 0.95, tone], axis=-1)
    return Image.fromarray(rgb.astype(np.uint8), "RGB").convert("RGBA")
