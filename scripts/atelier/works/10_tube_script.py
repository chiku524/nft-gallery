"""Neon tubing. Glass highlight, current flicker, no lettering."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageFilter

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=10,
    slug="tube-script",
    title="Tube Script",
    description="A glyph that is only glass and gas. The current travels; the word never arrives.",
    medium="Neon tube",
    motion="Flicker",
    palette="Magenta night",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    glow = Image.new("RGBA", (SIZE, SIZE), (8, 6, 14, 255))
    g = ImageDraw.Draw(glow)
    path = [
        (90, 360),
        (140, 140),
        (250, 300),
        (360, 120),
        (430, 350),
    ]
    on = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t * 3))
    color = (int(255 * on), int(70 * on), int(190 * on), 255)
    g.line(path, fill=color, width=22, joint="curve")
    glow = glow.filter(ImageFilter.GaussianBlur(10))
    tube = Image.new("RGBA", (SIZE, SIZE), (8, 6, 14, 255))
    tube.alpha_composite(glow)
    d = ImageDraw.Draw(tube)
    d.line(path, fill=(255, 210, 240, 255), width=6, joint="curve")
    d.line(path, fill=(255, 255, 255, 180), width=2, joint="curve")
    return tube
