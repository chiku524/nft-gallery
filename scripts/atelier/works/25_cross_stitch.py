"""Embroidery sampler. Counted X stitches, one row that finishes."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=25,
    slug="cross-stitch",
    title="Sampler Row",
    description="A counted cloth that never learned a picture. One row of X’s keeps arriving.",
    medium="Cross-stitch",
    motion="Sew",
    palette="Floss linen",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12
    canvas = Image.new("RGB", (SIZE, SIZE), (232, 220, 196))
    draw = ImageDraw.Draw(canvas)
    for x in range(36, 480, 16):
        draw.line((x, 36, x, 476), fill=(214, 200, 176), width=1)
    for y in range(36, 480, 16):
        draw.line((36, y, 476, y), fill=(214, 200, 176), width=1)
    floss = [(168, 36, 48), (36, 86, 120), (196, 148, 48), (64, 110, 78)]
    done = int(12 * 16 * t) + 8
    n = 0
    for row in range(12):
        for col in range(16):
            n += 1
            if n > done:
                continue
            x = 56 + col * 24
            y = 72 + row * 28
            color = floss[(row + col) % 4]
            draw.line((x, y, x + 14, y + 14), fill=color, width=3)
            draw.line((x + 14, y, x, y + 14), fill=color, width=3)
    return canvas.convert("RGBA")
