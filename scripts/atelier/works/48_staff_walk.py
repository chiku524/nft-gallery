"""Musical staff. Five lines, a black note that walks the measure."""

from __future__ import annotations

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=48,
    slug="staff-walk",
    title="Staff Walk",
    description="A measure with no key. The note keeps the appointment anyway.",
    medium="Notation",
    motion="Walk",
    palette="Score black",
)


def paint(frame: int) -> Image.Image:
    canvas = Image.new("RGB", (SIZE, SIZE), (242, 236, 220))
    draw = ImageDraw.Draw(canvas)
    for i in range(5):
        y = 180 + i * 28
        draw.line((40, y, 472, y), fill=(20, 20, 20), width=3)
    x = 70 + frame * 32
    y = 180 + (frame % 5) * 28
    draw.ellipse((x - 14, y - 10, x + 14, y + 10), fill=(16, 16, 16))
    draw.line((x + 12, y, x + 12, y - 70), fill=(16, 16, 16), width=4)
    return canvas.convert("RGBA")
