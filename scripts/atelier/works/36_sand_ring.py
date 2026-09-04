"""Sand mandala. Colored rings, one that rotates a grain-width."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=36,
    slug="sand-ring",
    title="Sand Ring",
    description="A mandala made to be swept. One ring turns before the broom arrives.",
    medium="Sand mandala",
    motion="Turn",
    palette="Temple dust",
)

RINGS = [(196, 48, 48), (36, 86, 168), (214, 176, 48), (48, 128, 86), (148, 64, 140)]


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (236, 220, 186))
    draw = ImageDraw.Draw(canvas)
    for i, color in enumerate(RINGS):
        r = 210 - i * 34
        draw.ellipse((256 - r, 256 - r, 256 + r, 256 + r), outline=color, width=16)
    rot = t
    for k in range(16):
        a = rot + k * math.tau / 16
        x = 256 + int(92 * math.cos(a))
        y = 256 + int(92 * math.sin(a))
        draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(214, 176, 48))
    return canvas.convert("RGBA")
