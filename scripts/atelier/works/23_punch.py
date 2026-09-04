"""Punch card. Cream stock, rectangular holes, a row that advances."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageFont

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=23,
    slug="punch",
    title="Punch",
    description="A card that stores nothing you can read. The holes advance; the meaning stays out.",
    medium="Punch card",
    motion="Advance",
    palette="Manila void",
)


def _font(size: int):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/consola.ttf", size)
    except OSError:
        return ImageFont.load_default()


PATTERN = [
    "1010010110100101",
    "0110101001011010",
    "1101001010110100",
    "0010110100101101",
    "1001011010010110",
    "0101101001011010",
    "1110010001110010",
    "0001101110001101",
]


def paint(frame: int) -> Image.Image:
    canvas = Image.new("RGB", (SIZE, SIZE), (42, 36, 30))
    draw = ImageDraw.Draw(canvas)
    card = Image.new("RGB", (440, 280), (226, 206, 164))
    c = ImageDraw.Draw(card)
    c.rectangle((0, 0, 439, 279), outline=(92, 72, 48), width=2)
    shift = frame % 8
    for row in range(8):
        bits = PATTERN[(row + shift) % 8]
        y = 36 + row * 28
        for col, bit in enumerate(bits):
            x = 28 + col * 24
            if bit == "1":
                c.rectangle((x, y, x + 14, y + 18), fill=(42, 36, 30))
            else:
                c.rectangle((x, y, x + 14, y + 18), outline=(150, 128, 90), width=1)
    c.text((16, 250), f"GOI 23   ROW {shift:02d}", font=_font(14), fill=(92, 72, 48))
    canvas.paste(card, (36, 116))
    draw.rectangle((20, 20, 492, 492), outline=(226, 206, 164), width=2)
    return canvas.convert("RGBA")
