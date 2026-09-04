"""Shipping waybill. Manila stock, a barcode that scans itself."""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=29,
    slug="waybill",
    title="Waybill",
    description="A label for a package that never left. The scan line is the journey.",
    medium="Barcode",
    motion="Scan",
    palette="Manila carbon",
)

BARS = "1101001001011010010110100101101001010110010100110100101"


def _font(size: int):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/consola.ttf", size)
    except OSError:
        return ImageFont.load_default()


def paint(frame: int) -> Image.Image:
    canvas = Image.new("RGB", (SIZE, SIZE), (48, 44, 40))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((48, 80, 464, 432), radius=8, fill=(226, 210, 168))
    draw.text((72, 100), "GOI  29  OPEN EDITION", font=_font(18), fill=(48, 40, 32))
    x = 72
    for i, bit in enumerate(BARS):
        w = 4 if bit == "1" else 2
        draw.rectangle((x, 170, x + w, 320), fill=(24, 20, 16))
        x += w + 2
    scan = 170 + ((frame * 13) % 150)
    draw.rectangle((68, scan, 444, scan + 4), fill=(220, 48, 48))
    draw.text((72, 360), "DEST  SALON   WT  1:1", font=_font(16), fill=(48, 40, 32))
    return canvas.convert("RGBA")
