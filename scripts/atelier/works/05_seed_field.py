"""Pointillist. Color only as dots. A traveling bloom, no contour."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=5,
    slug="seed-field",
    title="Seed Field",
    description="A meadow that is only dots. The bloom walks; the ground never draws a line.",
    medium="Pointillism",
    motion="Bloom walk",
    palette="Seed ochre",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (246, 232, 198))
    draw = ImageDraw.Draw(canvas)
    rng = np.random.default_rng(2026)
    xs = rng.integers(12, 500, 4200)
    ys = rng.integers(12, 500, 4200)
    cx = 256 + 90 * math.cos(t)
    cy = 256 + 70 * math.sin(t * 0.85)
    colors = np.array(
        [
            (196, 92, 48),
            (48, 110, 86),
            (214, 168, 64),
            (92, 64, 120),
            (232, 120, 88),
        ]
    )
    for i, (x, y) in enumerate(zip(xs, ys)):
        d = math.hypot(float(x) - cx, float(y) - cy)
        near = max(0.0, 1.0 - d / 160)
        tone = colors[i % len(colors)]
        if near > 0.15:
            tone = tuple(min(255, int(c + 50 * near)) for c in tone)
        r = 2 + int(3 * near)
        draw.ellipse((int(x) - r, int(y) - r, int(x) + r, int(y) + r), fill=tuple(int(c) for c in tone))
    return canvas.convert("RGBA")
