"""Construction barricade. Orange and white chevrons that crawl."""

from __future__ import annotations

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=38,
    slug="barricade",
    title="Barricade",
    description="A road closed to nothing. The stripes keep walking anyway.",
    medium="Barricade",
    motion="Crawl",
    palette="Safety orange",
)


def paint(frame: int) -> Image.Image:
    canvas = Image.new("RGB", (SIZE, SIZE), (246, 246, 242))
    draw = ImageDraw.Draw(canvas)
    shift = (frame * 14) % 80
    for i in range(-4, 16):
        x = i * 80 - shift
        draw.polygon([(x, 0), (x + 40, 0), (x + 40 + 512, 512), (x + 512, 512)], fill=(232, 92, 28))
    draw.rectangle((0, 0, 512, 36), fill=(18, 18, 18))
    draw.rectangle((0, 476, 512, 512), fill=(18, 18, 18))
    return canvas.convert("RGBA")
