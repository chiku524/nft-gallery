"""Carbon paper. Purple ghosts of a letter that was never sent."""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=37,
    slug="carbon-copy",
    title="Carbon Copy",
    description="A second sheet keeps a letter no one mailed. The words slip one row.",
    medium="Carbon paper",
    motion="Slip",
    palette="Violet tissue",
)


def _font(size: int):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", size)
    except OSError:
        return ImageFont.load_default()


LINES = [
    "dear salon",
    "the work is already",
    "elsewhere",
    "do not wait",
    "open edition",
]


def paint(frame: int) -> Image.Image:
    canvas = Image.new("RGB", (SIZE, SIZE), (228, 216, 196))
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    slip = (frame % 12) - 6
    for i, line in enumerate(LINES):
        draw.text((64, 90 + i * 64 + slip), line, font=_font(36), fill=(92, 36, 110, 200))
    layer = layer.filter(ImageFilter.GaussianBlur(0.6))
    out = canvas.convert("RGBA")
    out.alpha_composite(layer)
    return out
