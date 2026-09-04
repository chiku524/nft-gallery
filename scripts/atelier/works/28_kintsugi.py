"""Kintsugi. Dark ceramic shards, gold seams that brighten."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=28,
    slug="kintsugi",
    title="Kintsugi",
    description="A bowl that was already broken. The gold is the only part still deciding.",
    medium="Kintsugi",
    motion="Gleam",
    palette="Lacquer gold",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (18, 16, 14))
    draw = ImageDraw.Draw(canvas)
    draw.ellipse((70, 70, 442, 442), fill=(42, 32, 28))
    draw.ellipse((110, 110, 400, 400), fill=(28, 22, 20))
    gleam = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(t))
    gold = (int(196 + 50 * gleam), int(148 + 40 * gleam), int(48 + 20 * gleam))
    seams = [
        [(256, 80), (220, 200), (260, 320), (200, 430)],
        [(90, 220), (200, 240), (340, 210), (430, 260)],
        [(180, 120), (300, 280), (380, 400)],
    ]
    for path in seams:
        draw.line(path, fill=gold, width=5, joint="curve")
    return canvas.convert("RGBA")
