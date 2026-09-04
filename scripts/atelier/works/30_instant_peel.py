"""Instant film. White frame, a chemical that develops."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=30,
    slug="instant-peel",
    title="Instant Peel",
    description="A photograph that refuses a subject until the chemistry finishes. It never quite does.",
    medium="Instant film",
    motion="Develop",
    palette="Peel chemistry",
)


def paint(frame: int) -> Image.Image:
    t = (frame + 1) / 12
    canvas = Image.new("RGB", (SIZE, SIZE), (28, 26, 24))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((70, 48, 442, 464), fill=(236, 232, 224))
    yy, xx = np.mgrid[0:300, 0:336].astype(np.float32)
    scene = 80 + 40 * np.sin(xx * 0.03) * np.cos(yy * 0.025)
    sky = np.clip(140 + (300 - yy) * 0.2, 0, 255)
    develop = np.clip((yy / 300) - (1.0 - t) * 1.2, 0, 1)
    rgb = np.stack(
        [sky * (1 - develop) + scene * develop, sky * 0.9 * (1 - develop) + (scene * 0.7) * develop, sky * 0.7 * (1 - develop) + (scene * 0.4) * develop],
        axis=-1,
    )
    window = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")
    canvas.paste(window, (88, 66))
    draw.rectangle((70, 380, 442, 464), fill=(236, 232, 224))
    return canvas.convert("RGBA")
