"""Cork board. Tan field, pins that hop to new holes."""

from __future__ import annotations

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=46,
    slug="cork-pins",
    title="Cork Pins",
    description="A board that never held a note. The pins keep finding new holes.",
    medium="Cork",
    motion="Hop",
    palette="Tan pin",
)

PINS = [(196, 36, 36), (36, 86, 168), (214, 168, 36), (48, 110, 64), (148, 48, 110)]


def paint(frame: int) -> Image.Image:
    canvas = Image.new("RGB", (SIZE, SIZE), (186, 148, 86))
    draw = ImageDraw.Draw(canvas)
    for y in range(20, 500, 8):
        for x in range(20 + (y % 16), 500, 16):
            draw.point((x, y), fill=(160, 120, 64))
    for i, color in enumerate(PINS):
        x = 80 + ((i * 70 + frame * 17) % 360)
        y = 90 + ((i * 53 + frame * 11) % 320)
        draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=color)
        draw.line((x, y, x + 4, y + 18), fill=(40, 40, 40), width=2)
    return canvas.convert("RGBA")
