"""Ben-Day comic. CMYK dots, one plate that pulses."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=31,
    slug="ben-day",
    title="Ben-Day",
    description="Four cheap inks pretending to be a sky. The cyan plate keeps arriving late.",
    medium="Ben-Day",
    motion="Pulse",
    palette="Process CMYK",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (246, 242, 230))
    draw = ImageDraw.Draw(canvas)
    cyan_r = 5 + int(3 * (0.5 + 0.5 * math.sin(t)))
    for y in range(20, 500, 14):
        for x in range(20, 500, 14):
            draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(0, 160, 214))
    for y in range(28, 500, 18):
        for x in range(28, 500, 18):
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(220, 20, 90))
    for y in range(40, 500, 22):
        for x in range(16, 500, 22):
            draw.ellipse((x - cyan_r, y - cyan_r, x + cyan_r, y + cyan_r), fill=(20, 180, 200))
    draw.rectangle((80, 80, 432, 432), outline=(18, 18, 18), width=10)
    return canvas.convert("RGBA")
