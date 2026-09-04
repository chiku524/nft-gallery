"""Regulatory enamel. A yellow triangle that refuses traffic."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=35,
    slug="yield-field",
    title="Yield Field",
    description="A sign with no road. The warning is the whole landscape.",
    medium="Traffic enamel",
    motion="Warn",
    palette="Safety yellow",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (28, 72, 36))
    draw = ImageDraw.Draw(canvas)
    pulse = int(8 * math.sin(t))
    draw.polygon([(256, 70 - pulse), (450 + pulse, 430), (62 - pulse, 430)], fill=(246, 206, 28), outline=(18, 18, 18))
    draw.polygon([(256, 130), (400, 400), (112, 400)], outline=(18, 18, 18), width=18)
    return canvas.convert("RGBA")
