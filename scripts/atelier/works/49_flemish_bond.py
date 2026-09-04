"""Flemish brick. A wall, one stretcher that darkens after rain."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=49,
    slug="flemish-bond",
    title="Flemish Bond",
    description="A wall that is only the wall. One brick remembers weather.",
    medium="Brick",
    motion="Weather",
    palette="Clay mortar",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (196, 186, 168))
    draw = ImageDraw.Draw(canvas)
    wet = int(30 * (0.5 + 0.5 * math.sin(t)))
    for row in range(12):
        offset = 0 if row % 2 == 0 else 36
        for col in range(9):
            x = offset + col * 72
            y = 16 + row * 40
            color = (156, 64, 48)
            if row == 5 and col == 3:
                color = (156 - wet, 64 - wet // 2, 48 - wet // 3)
            draw.rectangle((x, y, x + 68, y + 36), fill=color, outline=(196, 186, 168))
    return canvas.convert("RGBA")
