"""Garter stitch. Yarn loops, a needle that claims the next row."""

from __future__ import annotations

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=43,
    slug="garter-knit",
    title="Garter Knit",
    description="A scarf that is only rows. The needle is still working the last one.",
    medium="Knit",
    motion="Cast",
    palette="Wool rust",
)


def paint(frame: int) -> Image.Image:
    canvas = Image.new("RGB", (SIZE, SIZE), (86, 36, 28))
    draw = ImageDraw.Draw(canvas)
    live = frame % 12
    for row in range(14):
        y = 40 + row * 32
        wool = (196, 92, 64) if row <= live else (140, 60, 48)
        for x in range(36, 480, 22):
            draw.arc((x, y, x + 20, y + 24), 200, 340, fill=wool, width=4)
            draw.arc((x + 4, y + 8, x + 24, y + 28), 20, 160, fill=wool, width=4)
    draw.line((40, 40 + live * 32, 470, 40 + live * 32), fill=(220, 220, 214), width=3)
    return canvas.convert("RGBA")
