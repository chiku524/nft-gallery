"""Herbarium plate. Scientific contour, caption, one vein that settles."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageFont

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=11,
    slug="pressed-leaf",
    title="Pressed Leaf",
    description="A specimen plate with no garden behind it. The midrib darkens as the press holds.",
    medium="Herbarium ink",
    motion="Settle",
    palette="Plate umber",
)


def _font(size: int):
    for path in ("C:/Windows/Fonts/georgia.ttf", "C:/Windows/Fonts/times.ttf"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (236, 228, 210))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((28, 28, 484, 484), outline=(92, 72, 48), width=2)
    draw.rectangle((36, 36, 476, 476), outline=(168, 148, 118), width=1)
    ink = (62, 48, 32)
    cx, cy = 256, 230
    sway = 4 * math.sin(t)
    draw.line((cx, 390, cx + sway, 96), fill=ink, width=3)
    for i, side in enumerate((-1, 1)):
        for k in range(7):
            y = 130 + k * 34
            length = 70 + (k % 3) * 18
            draw.line((cx + sway, y, cx + sway + side * length, y - 18 + k), fill=ink, width=2)
            draw.polygon(
                [
                    (cx + sway + side * 8, y),
                    (cx + sway + side * length, y - 20),
                    (cx + sway + side * (length - 10), y + 10),
                ],
                outline=ink,
            )
    settle = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t))
    mid = tuple(int(c * (0.45 + 0.55 * settle)) for c in ink)
    draw.line((cx + sway, 380, cx + sway, 110), fill=mid, width=2)
    draw.text((52, 430), "No. 11   •   undetermined frond   •   open edition", font=_font(16), fill=ink)
    return canvas.convert("RGBA")
