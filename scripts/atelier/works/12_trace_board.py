"""PCB. Solder mask, gold pads, a trace that powers on."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=12,
    slug="trace-board",
    title="Trace Board",
    description="A board with no device. Gold pads wait. One trace finally takes current.",
    medium="Solder mask",
    motion="Current",
    palette="Mask gold",
)


def paint(frame: int) -> Image.Image:
    t = frame / 12
    canvas = Image.new("RGB", (SIZE, SIZE), (16, 56, 36))
    draw = ImageDraw.Draw(canvas)
    mask = (22, 78, 48)
    gold = (212, 168, 64)
    silk = (214, 220, 196)
    for x in range(48, 470, 56):
        for y in range(48, 470, 56):
            draw.rectangle((x - 6, y - 6, x + 6, y + 6), fill=gold)
    traces = [
        [(64, 64), (64, 256), (200, 256), (200, 400)],
        [(448, 64), (320, 64), (320, 200), (448, 200), (448, 448)],
        [(120, 448), (280, 448), (280, 120)],
    ]
    live = int(t * 12) % 3
    for i, path in enumerate(traces):
        color = (120, 210, 90) if i == live else mask
        draw.line(path, fill=color, width=8, joint="curve")
    draw.ellipse((232, 232, 280, 280), outline=gold, width=4)
    draw.text((40, 14), "STRNGR  12  REV A", fill=silk)
    return canvas.convert("RGBA")
