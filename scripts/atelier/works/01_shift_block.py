"""Hard-edge enamel. Flat primaries, no blend, one sliding slab."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=1,
    slug="shift-block",
    title="Shift Block",
    description="Three enamel slabs refuse to share an edge. The red one keeps the beat.",
    medium="Hard-edge enamel",
    motion="Slide",
    palette="Primary enamel",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (244, 240, 232))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 512, 84), fill=(18, 18, 18))
    draw.rectangle((0, 428, 512, 512), fill=(18, 18, 18))
    draw.rectangle((36, 110, 210, 400), fill=(18, 62, 168))
    draw.rectangle((302, 110, 476, 400), fill=(232, 196, 28))
    slide = int(48 * math.sin(t))
    draw.rectangle((196 + slide, 168, 316 + slide, 348), fill=(196, 28, 36))
    draw.rectangle((0, 84, 512, 92), fill=(18, 18, 18))
    draw.rectangle((0, 420, 512, 428), fill=(18, 18, 18))
    return canvas.convert("RGBA")
