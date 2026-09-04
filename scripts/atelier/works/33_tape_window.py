"""Cassette window. Two reels trading brown tape."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=33,
    slug="tape-window",
    title="Tape Window",
    description="A cassette that never plays a song. The reels keep the only motion.",
    medium="Cassette",
    motion="Reel",
    palette="Smoke brown",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (22, 22, 24))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((48, 110, 464, 402), radius=18, fill=(48, 48, 52))
    draw.rectangle((90, 170, 422, 330), fill=(12, 10, 10))
    left_pack = 70 + int(18 * math.sin(t))
    right_pack = 70 - int(18 * math.sin(t))
    draw.ellipse((130 - left_pack, 210 - left_pack + 40, 130 + left_pack + 80, 210 + left_pack + 40), outline=(92, 64, 36), width=14)
    draw.ellipse((300 - right_pack, 210 - right_pack + 40, 300 + right_pack + 80, 210 + right_pack + 40), outline=(92, 64, 36), width=14)
    for cx in (170, 340):
        ang = t if cx == 170 else -t
        for i in range(6):
            a = ang + i * math.tau / 6
            draw.line((cx, 250, cx + int(28 * math.cos(a)), 250 + int(28 * math.sin(a))), fill=(180, 180, 184), width=3)
        draw.ellipse((cx - 12, 238, cx + 12, 262), fill=(200, 200, 204))
    return canvas.convert("RGBA")
