"""Teletype roll. Green columns on black, a cursor that eats the next glyph."""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=27,
    slug="teletype",
    title="Teletype",
    description="A roll of unused language. The cursor is the only reader.",
    medium="Teletype",
    motion="Advance",
    palette="Terminal green",
)

GLYPHS = "GOI#*+=/\\<>^v~01"


def _font(size: int):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/consola.ttf", size)
    except OSError:
        return ImageFont.load_default()


def paint(frame: int) -> Image.Image:
    canvas = Image.new("RGB", (SIZE, SIZE), (6, 10, 8))
    draw = ImageDraw.Draw(canvas)
    font = _font(22)
    live = frame % 12
    for row in range(16):
        line = "".join(GLYPHS[(row * 5 + col + frame) % len(GLYPHS)] for col in range(18))
        y = 28 + row * 30
        color = (72, 220, 110) if row == 4 + live % 8 else (28, 86, 48)
        draw.text((28, y), line, font=font, fill=color)
    draw.rectangle((28, 28 + (4 + live % 8) * 30, 40, 48 + (4 + live % 8) * 30), fill=(180, 255, 190))
    return canvas.convert("RGBA")
