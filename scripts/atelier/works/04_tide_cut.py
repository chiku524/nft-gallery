"""Woodcut. Cream paper, carved black gouges, no gradients."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=4,
    slug="tide-cut",
    title="Tide Cut",
    description="A block of cream paper takes the tide in carved strokes. Nothing here blends.",
    medium="Woodcut",
    motion="Gouge",
    palette="Sumi cream",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (236, 224, 198))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((22, 22, 490, 490), outline=(22, 18, 14), width=10)
    phase = 18 * math.sin(t)
    for row in range(16):
        y = 56 + row * 26
        amp = 22 + (row % 4) * 6
        points: list[tuple[int, int]] = []
        for x in range(48, 468, 8):
            wobble = amp * math.sin((x + phase + row * 18) * 0.035)
            points.append((x, int(y + wobble)))
        draw.line(points, fill=(22, 18, 14), width=3 + row % 2)
    draw.polygon([(80, 400), (250, 250 + 12 * math.sin(t)), (430, 410)], outline=(22, 18, 14))
    for x in range(90, 430, 14):
        draw.line((x, 408, x + 4, 250 + int(10 * math.sin(t + x * 0.04))), fill=(22, 18, 14), width=2)
    return canvas.convert("RGBA")
