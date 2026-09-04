"""Letterpress lockup. A giant glyph, ink squash, an impression that deepens."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=19,
    slug="lockup",
    title="Lockup",
    description="One letter takes the whole chase. The impression deepens; the alphabet stays out of it.",
    medium="Letterpress",
    motion="Impression",
    palette="Bone vermilion",
)


def _font(size: int):
    for path in ("C:/Windows/Fonts/georgia.ttf", "C:/Windows/Fonts/timesbd.ttf", "C:/Windows/Fonts/arialbd.ttf"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    paper = Image.new("RGB", (SIZE, SIZE), (236, 226, 208))
    depth = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t))
    stamp = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(stamp)
    draw.text((86, 48), "S", font=_font(420), fill=(168, 28, 36, int(230 * depth)))
    offset = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(offset).text((92, 56), "S", font=_font(420), fill=(40, 28, 22, int(70 * depth)))
    offset = offset.filter(ImageFilter.GaussianBlur(2))
    out = paper.convert("RGBA")
    out.alpha_composite(offset)
    out.alpha_composite(stamp)
    return out
