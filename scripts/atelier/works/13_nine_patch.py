"""Quilt nine-patch. Stitched blocks, fabric grain, one square breathing."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=13,
    slug="nine-patch",
    title="Nine Patch",
    description="Nine fabrics share a seam allowance. The center square keeps inhaling thread.",
    medium="Quilt",
    motion="Stitch",
    palette="Calico",
)


PATCHES = [
    (168, 48, 52),
    (48, 92, 110),
    (210, 154, 64),
    (92, 56, 86),
    (236, 214, 186),
    (64, 110, 72),
    (186, 86, 48),
    (40, 48, 64),
    (214, 120, 98),
]


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (46, 36, 32))
    draw = ImageDraw.Draw(canvas)
    cell = 148
    origin = 34
    for i, color in enumerate(PATCHES):
        col, row = i % 3, i // 3
        x0 = origin + col * cell
        y0 = origin + row * cell
        fill = color
        if i == 4:
            pulse = int(18 * math.sin(t))
            fill = tuple(max(0, min(255, c + pulse)) for c in color)
        draw.rectangle((x0, y0, x0 + cell - 8, y0 + cell - 8), fill=fill)
        for s in range(8, cell - 12, 10):
            draw.line((x0 + s, y0 + 4, x0 + s, y0 + cell - 12), fill=(255, 255, 255, 40), width=1)
        draw.rectangle((x0, y0, x0 + cell - 8, y0 + cell - 8), outline=(236, 224, 208), width=3)
        for stitch in range(6, cell - 14, 8):
            draw.line((x0 + stitch, y0 + 2, x0 + stitch + 3, y0 + 2), fill=(236, 224, 208), width=2)
    return canvas.convert("RGBA")
