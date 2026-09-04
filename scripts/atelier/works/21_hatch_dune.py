"""Contour hatch. Sepia topography, wind that shifts the lines."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=21,
    slug="hatch-dune",
    title="Hatch Dune",
    description="A map of a place that is only height. The wind rewrites the contours.",
    medium="Contour hatch",
    motion="Wind",
    palette="Sepia dust",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (232, 214, 186))
    draw = ImageDraw.Draw(canvas)
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    height = (
        np.sin((xx + 20 * math.sin(t)) * 0.012) * np.cos(yy * 0.01)
        + 0.45 * np.sin((xx * 0.02) - (yy * 0.015) + t)
    )
    levels = np.linspace(height.min(), height.max(), 14)
    ink = (92, 62, 36)
    for level in levels[1:-1]:
        mask = np.abs(height - level) < 0.045
        ys, xs = np.where(mask)
        if len(xs) == 0:
            continue
        for x, y in zip(xs[::7], ys[::7]):
            draw.point((int(x), int(y)), fill=ink)
    draw.rectangle((24, 24, 488, 488), outline=ink, width=2)
    return canvas.convert("RGBA")
