"""Microfiche. Amber negative, inverted blocks that slide a row."""

from __future__ import annotations

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=42,
    slug="microfiche",
    title="Microfiche",
    description="A library reduced to amber. One row of ghosts advances.",
    medium="Microfiche",
    motion="Index",
    palette="Amber negative",
)


def paint(frame: int) -> Image.Image:
    canvas = Image.new("RGB", (SIZE, SIZE), (48, 28, 10))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((36, 36, 476, 476), fill=(186, 120, 36))
    shift = frame % 6
    for row in range(6):
        for col in range(5):
            x0 = 56 + col * 82
            y0 = 56 + ((row + shift) % 6) * 70
            draw.rectangle((x0, y0, x0 + 70, y0 + 56), fill=(32, 18, 8))
            draw.rectangle((x0 + 8, y0 + 10, x0 + 62, y0 + 18), fill=(186, 120, 36))
            draw.rectangle((x0 + 8, y0 + 26, x0 + 48, y0 + 32), fill=(186, 120, 36))
    return canvas.convert("RGBA")
