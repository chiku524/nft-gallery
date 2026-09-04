"""Maritime pennants. A clothesline of signals, one flag that snaps."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=41,
    slug="pennant-line",
    title="Pennant Line",
    description="Flags that name no ship. One pennant keeps changing its mind in the wind.",
    medium="Maritime flag",
    motion="Snap",
    palette="Signal cloth",
)

FLAGS = [(196, 28, 36), (28, 62, 148), (246, 206, 28), (236, 236, 236), (36, 110, 64)]


def paint(frame: int) -> Image.Image:
    t = frame / 12 * math.tau
    canvas = Image.new("RGB", (SIZE, SIZE), (140, 186, 214))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 300, 512, 512), fill=(36, 86, 120))
    draw.line((40, 120, 470, 140), fill=(40, 32, 24), width=6)
    for i, color in enumerate(FLAGS):
        x = 70 + i * 80
        flap = int(10 * math.sin(t + i)) if i == 2 else 0
        draw.polygon([(x, 128), (x + 54 + flap, 150), (x, 210)], fill=color, outline=(20, 20, 20))
    return canvas.convert("RGBA")
