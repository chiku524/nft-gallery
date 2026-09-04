"""Leaded glass. Thick cames, flat jewel panes, one pane that cycles."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=22,
    slug="lead-light",
    title="Lead Light",
    description="Jewel glass held by lead. No glow, no wash — only a pane that changes its mind.",
    medium="Leaded glass",
    motion="Cycle",
    palette="Jewel lead",
)


PANES = [
    ((40, 40, 200, 220), (164, 28, 48)),
    ((200, 40, 360, 180), (28, 72, 148)),
    ((360, 40, 472, 240), (214, 168, 36)),
    ((40, 220, 180, 472), (36, 110, 86)),
    ((180, 180, 320, 340), (196, 86, 42)),
    ((320, 180, 472, 360), (92, 48, 120)),
    ((180, 340, 360, 472), (48, 128, 148)),
    ((360, 360, 472, 472), (214, 92, 78)),
    ((40, 40, 472, 472), None),
]


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (18, 16, 16))
    draw = ImageDraw.Draw(canvas)
    cycle = [
        (164, 28, 48),
        (28, 72, 148),
        (214, 168, 36),
        (36, 110, 86),
    ]
    live = cycle[int((frame / 12) * len(cycle)) % len(cycle)]
    for i, (box, color) in enumerate(PANES[:-1]):
        fill = live if i == 4 else color
        if i == 4:
            mix = 0.5 + 0.5 * math.sin(t)
            fill = tuple(int(a * (1 - mix) + b * mix) for a, b in zip(color, live))
        draw.rectangle(box, fill=fill)
    draw.line((40, 40, 472, 40, 472, 472, 40, 472, 40, 40), fill=(16, 16, 16), width=14)
    draw.line((200, 40, 200, 472), fill=(16, 16, 16), width=12)
    draw.line((360, 40, 360, 472), fill=(16, 16, 16), width=12)
    draw.line((40, 220, 472, 220), fill=(16, 16, 16), width=12)
    draw.line((40, 340, 472, 340), fill=(16, 16, 16), width=12)
    draw.line((180, 180, 320, 180, 320, 340, 180, 340, 180, 180), fill=(16, 16, 16), width=10)
    return canvas.convert("RGBA")
