"""Ikat warp. Dyed stripes that miss their register."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=32,
    slug="ikat-shift",
    title="Ikat Shift",
    description="A warp that was tied before it was dyed. The miss is the pattern.",
    medium="Ikat",
    motion="Slip",
    palette="Warp indigo",
)

STRIPE = [(36, 48, 92), (196, 86, 42), (214, 186, 92), (36, 48, 92), (168, 48, 64)]


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (28, 24, 32))
    draw = ImageDraw.Draw(canvas)
    for x in range(0, SIZE, 18):
        color = STRIPE[(x // 18) % len(STRIPE)]
        slip = int(16 * math.sin(t + x * 0.04))
        draw.rectangle((x, 0, x + 16, SIZE), fill=color)
        draw.rectangle((x, 180 + slip, x + 16, 340 + slip), fill=tuple(min(255, c + 40) for c in color))
    return canvas.convert("RGBA")
