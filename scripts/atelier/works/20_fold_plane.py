"""Crease pattern. Mountain and valley, one fold that breathes."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=20,
    slug="fold-plane",
    title="Fold Plane",
    description="A sheet that has already been thought through. One valley keeps changing its mind.",
    medium="Crease pattern",
    motion="Breathe",
    palette="Paper graphite",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (248, 244, 236))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((40, 40, 472, 472), outline=(40, 40, 40), width=3)
    valleys = [
        [(40, 256), (472, 256)],
        [(256, 40), (256, 472)],
        [(40, 40), (472, 472)],
        [(472, 40), (40, 472)],
    ]
    for path in valleys:
        draw.line(path, fill=(90, 90, 90), width=2)
    mountains = [
        [(40, 148), (472, 148)],
        [(40, 364), (472, 364)],
        [(148, 40), (148, 472)],
        [(364, 40), (364, 472)],
    ]
    for path in mountains:
        draw.line(path, fill=(40, 40, 40), width=1)
    breath = int(18 * math.sin(t))
    draw.polygon(
        [(256, 148 + breath), (364, 256), (256, 364 - breath), (148, 256)],
        outline=(18, 18, 18),
        fill=(228, 220, 208),
    )
    draw.line((256, 148 + breath, 256, 364 - breath), fill=(18, 18, 18), width=2)
    return canvas.convert("RGBA")
