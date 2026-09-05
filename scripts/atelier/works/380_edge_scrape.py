"""Mezzotint crop. Independent salon work 380."""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from atelier.surface import WorkSpec

SIZE = 512
WORK = WorkSpec(
    id=380,
    slug='edge-scrape',
    title='Edge Scrape',
    description='A fragment of a dark.',
    medium='Mezzotint crop',
    motion='Crop',
    palette='Edge copper',
)

def paint(frame: int) -> Image.Image:

    t = frame / 12 * math.tau
    bg, ink, accent, mid = (111, 243, 22), (144, 12, 233), (88, 130, 71), (127, 127, 127)
    scale, ox, oy, spin = 1.280, 80, -50, -0.500
    canvas = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(canvas)
    
    yy, xx = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    tooth = (np.sin(xx * 0.35) * np.sin(yy * 0.35) > 0).astype(np.float32)
    light = np.exp(-((xx - 260 - 20 * math.cos(t)) ** 2 + (yy - 220) ** 2) / (9000 * scale))
    mix = np.clip(tooth * 0.45 + light, 0, 1)
    rgb = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    for c in range(3):
        rgb[..., c] = ink[c] + (bg[c] - ink[c]) * mix
    canvas = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")
    draw = ImageDraw.Draw(canvas)
    
    return canvas.convert("RGBA")
