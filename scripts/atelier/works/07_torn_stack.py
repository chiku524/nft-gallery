"""Torn-paper collage. Deckled scraps, stacked stock, one piece lifts."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageFilter

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=7,
    slug="torn-stack",
    title="Torn Stack",
    description="Four leftover sheets refuse a tidy stack. One scrap keeps leaving the pile.",
    medium="Paper collage",
    motion="Lift",
    palette="Scrap stock",
)


def _scrap(size: tuple[int, int], color: tuple[int, int, int], seed: int) -> Image.Image:
    w, h = size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    pts: list[tuple[int, int]] = []
    steps = 28
    for i in range(steps):
        a = i / steps * math.tau
        r = 0.42 + 0.08 * math.sin(seed * 1.7 + i * 1.9)
        pts.append((int(w * (0.5 + r * math.cos(a))), int(h * (0.5 + r * math.sin(a)))))
    draw.polygon(pts, fill=(*color, 255))
    return layer.filter(ImageFilter.GaussianBlur(0.4))


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGBA", (SIZE, SIZE), (38, 34, 32, 255))
    scraps = [
        ((40, 50), (340, 300), (198, 92, 64), 3),
        ((160, 80), (320, 280), (236, 214, 170), 7),
        ((70, 200), (300, 260), (64, 92, 110), 11),
        ((190, 190), (280, 250), (214, 154, 72), 19),
    ]
    for i, ((x, y), size, color, seed) in enumerate(scraps):
        piece = _scrap(size, color, seed)
        lift = 0
        if i == 3:
            lift = int(16 * math.sin(t))
            piece = piece.rotate(8 * math.sin(t), resample=Image.Resampling.BICUBIC, expand=True)
        alpha = piece.split()[-1]
        shadow = Image.new("RGBA", piece.size, (0, 0, 0, 0))
        shadow.paste((0, 0, 0, 60), mask=alpha)
        canvas.alpha_composite(shadow, (x + 8, y + 10 + lift))
        canvas.alpha_composite(piece, (x, y + lift))
    return canvas
