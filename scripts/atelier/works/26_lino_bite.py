"""Linocut. Flat crimson on black, a carved bird that hops one cut."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=26,
    slug="lino-bite",
    title="Lino Bite",
    description="A block of linoleum keeps one animal. The beak advances a cut at a time.",
    medium="Linocut",
    motion="Hop",
    palette="Crimson block",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (16, 12, 12))
    draw = ImageDraw.Draw(canvas)
    lift = int(10 * math.sin(t))
    draw.ellipse((90, 160 + lift, 360, 390 + lift), fill=(176, 28, 36))
    draw.polygon([(340, 250 + lift), (470, 230 + lift), (350, 300 + lift)], fill=(176, 28, 36))
    draw.polygon([(180, 170 + lift), (250, 70 + lift), (270, 190 + lift)], fill=(176, 28, 36))
    draw.ellipse((210, 230 + lift, 250, 270 + lift), fill=(16, 12, 12))
    for y in range(400, 480, 10):
        draw.line((40, y, 470, y + 6), fill=(176, 28, 36), width=4)
    return canvas.convert("RGBA")
