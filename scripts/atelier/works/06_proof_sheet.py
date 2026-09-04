"""Cyanotype proof. Prussian field, white construction, a line that draws itself."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageFont

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=6,
    slug="proof-sheet",
    title="Proof Sheet",
    description="A construction that never became a building. The white line is still deciding.",
    medium="Cyanotype",
    motion="Draw",
    palette="Prussian white",
)


def _font(size: int):
    for path in ("C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def paint(frame: int) -> Image.Image:
    t = frame / 12
    canvas = Image.new("RGB", (SIZE, SIZE), (18, 62, 118))
    draw = ImageDraw.Draw(canvas)
    for x in range(32, 480, 24):
        draw.line((x, 48, x, 464), fill=(56, 110, 168), width=1)
    for y in range(48, 480, 24):
        draw.line((32, y, 480, y), fill=(56, 110, 168), width=1)
    draw.rectangle((32, 48, 480, 464), outline=(230, 238, 246), width=2)
    draw.rectangle((32, 428, 480, 464), outline=(230, 238, 246), width=1)
    draw.text((44, 434), "SHEET 06  ·  OPEN EDITION  ·  NOT FOR BUILD", font=_font(14), fill=(230, 238, 246))
    progress = 0.12 + 0.88 * ((math.sin(t * math.tau) + 1) / 2)
    x0, y0, x1, y1 = 96, 360, 400, 120
    x = x0 + (x1 - x0) * progress
    y = y0 + (y1 - y0) * progress
    draw.line((x0, y0, x, y), fill=(236, 244, 250), width=3)
    draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(236, 244, 250))
    draw.rectangle((110, 150, 250, 300), outline=(230, 238, 246), width=2)
    draw.polygon([(280, 300), (360, 140), (430, 300)], outline=(230, 238, 246))
    return canvas.convert("RGBA")
