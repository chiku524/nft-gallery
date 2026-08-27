#!/usr/bin/env python3
"""Rebuild trait PNGs with correct alpha and pug-relative placement.

Bases: flood-fill white from the edges only so cream/fawn fur stays opaque.
Hats, body, accessories: knock out all white (including interior holes), crop
to content, and paste onto a 1024 canvas at pug landmarks so the studio and
the 10k generator can stack layers 1:1.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = Path("/opt/cursor/artifacts/assets")
DST = ROOT / "public" / "traits"
SIZE = 1024
TEST_DIR = ROOT / "generated" / "placement-tests"


def flood_white(im: Image.Image, thresh: int = 246) -> Image.Image:
    """Transparent only for near-white pixels connected to the canvas edge."""
    arr = np.array(im.convert("RGBA"))
    rgb = arr[..., :3].astype(np.int16)
    h, w = rgb.shape[:2]
    white = rgb.min(axis=2) >= thresh
    visited = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()

    def push(y: int, x: int) -> None:
        if 0 <= y < h and 0 <= x < w and white[y, x] and not visited[y, x]:
            visited[y, x] = True
            q.append((y, x))

    for x in range(w):
        push(0, x)
        push(h - 1, x)
    for y in range(h):
        push(y, 0)
        push(y, w - 1)

    while q:
        y, x = q.popleft()
        arr[y, x, 3] = 0
        push(y - 1, x)
        push(y + 1, x)
        push(y, x - 1)
        push(y, x + 1)

    return Image.fromarray(arr, "RGBA")


def knock_all_white(im: Image.Image, thresh: int = 246) -> Image.Image:
    """Transparent for every near-white pixel (opens bandana/chain holes)."""
    arr = np.array(im.convert("RGBA"))
    white = arr[..., :3].min(axis=2) >= thresh
    arr[..., 3] = np.where(white, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def content_crop(im: Image.Image, pad: int = 2) -> Image.Image:
    arr = np.array(im)
    ys, xs = np.where(arr[..., 3] > 12)
    if len(xs) == 0:
        return im
    left, right = max(0, xs.min() - pad), min(im.width - 1, xs.max() + pad)
    top, bottom = max(0, ys.min() - pad), min(im.height - 1, ys.max() + pad)
    return im.crop((left, top, right + 1, bottom + 1))


def paste_centered(canvas: Image.Image, overlay: Image.Image, cx: int, cy: int) -> None:
    x = int(cx - overlay.width / 2)
    y = int(cy - overlay.height / 2)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ox, oy = overlay.size
    src_x, src_y = max(0, -x), max(0, -y)
    dst_x, dst_y = max(0, x), max(0, y)
    width = min(ox - src_x, canvas.width - dst_x)
    height = min(oy - src_y, canvas.height - dst_y)
    if width <= 0 or height <= 0:
        return
    cropped = overlay.crop((src_x, src_y, src_x + width, src_y + height))
    layer.paste(cropped, (dst_x, dst_y), cropped)
    canvas.alpha_composite(layer)


def paste_bottom(canvas: Image.Image, overlay: Image.Image, cx: int, bottom: int) -> None:
    paste_centered(canvas, overlay, cx, bottom - overlay.height / 2)


def fit_width(im: Image.Image, width: int) -> Image.Image:
    if im.width == 0:
        return im
    height = max(1, round(im.height * (width / im.width)))
    return im.resize((width, height), Image.Resampling.LANCZOS)


def fit_height(im: Image.Image, height: int) -> Image.Image:
    if im.height == 0:
        return im
    width = max(1, round(im.width * (height / im.height)))
    return im.resize((width, height), Image.Resampling.LANCZOS)


def boost_fill(im: Image.Image, tan: tuple[float, float, float], mix: float) -> Image.Image:
    """Pull pale fur toward a readable tan so heads don't vanish on busy backgrounds."""
    arr = np.array(im).astype(np.float32)
    rgb = arr[..., :3]
    alpha = arr[..., 3]
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    rows = np.arange(arr.shape[0])[:, None]
    fill = (alpha > 200) & (rows < 640) & (chroma > 15) & (rgb.min(axis=2) > 80)
    target = np.array(tan, dtype=np.float32)
    rgb[fill] = rgb[fill] * (1.0 - mix) + target * mix
    arr[..., :3] = np.clip(rgb, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def save(im: Image.Image, rel: str) -> None:
    path = DST / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)
    arr = np.array(im)
    print(f"  {rel} opaque={((arr[..., 3] > 12).mean()*100):.1f}%")


# Hats sit on the crown: brim aligned near the top of the skull.
HATS = {
    "hat/hat-beanie.png": ("hat-only-beanie.png", 290, 352),
    "hat/hat-crown.png": ("hat-only-crown.png", 210, 328),
    "hat/hat-snapback.png": ("hat-only-snapback.png", 300, 358),
    "hat/hat-newsie.png": ("hat-only-newsie.png", 290, 350),
    "hat/hat-hardhat.png": ("hat-only-hardhat.png", 280, 342),
}

# Neck items sit at the wall line, under the chin — not over the face.
BODIES = {
    "body/body-bandana.png": ("body-bandana.png", 230, 648),
    "body/body-collar.png": ("body-collar.png", 220, 658),
    "body/body-hoodie.png": ("body-hoodie.png", 260, 670),
    "body/body-gold-chain.png": ("body-gold-chain.png", 200, 652),
}

ACCESSORIES = {
    "accessory/acc-sunglasses.png": ("acc-sunglasses.png", "eyes", 240, 400),
    "accessory/acc-monocle.png": ("acc-monocle.png", "eye", 110, 390),
    "accessory/acc-coffee.png": ("acc-coffee.png", "ledge", 110, 655),
    "accessory/acc-bone.png": ("acc-bone.png", "ledge", 140, 655),
    "accessory/acc-blocks.png": ("acc-blocks.png", "ledge", 140, 665),
}

BASES = {
    "base/base-fawn-peek.png": "base-fawn-peek.png",
    "base/base-cream-peek.png": "base-cream-peek.png",
    "base/base-black-peek.png": "base-black-peek.png",
}

BLOCKS = {
    "block/block-concrete.png": "block-concrete.png",
    "block/block-brownstone.png": "block-brownstone.png",
    "block/block-crate.png": "block-crate.png",
    "block/block-gold.png": "block-gold.png",
}


def prepare() -> None:
    print("Bases (edge flood-fill)…")
    boosts = {
        "base/base-fawn-peek.png": ((214, 168, 128), 0.22),
        "base/base-cream-peek.png": ((228, 186, 142), 0.38),
        "base/base-black-peek.png": None,
    }
    for dest, src in BASES.items():
        prepared = flood_white(Image.open(SRC / src))
        extra = boosts[dest]
        if extra:
            prepared = boost_fill(prepared, extra[0], extra[1])
        save(prepared, dest)

    print("Blocks (edge flood-fill)…")
    for dest, src in BLOCKS.items():
        save(flood_white(Image.open(SRC / src)), dest)

    print("Hats (crop + place on crown)…")
    for dest, (src, width, bottom) in HATS.items():
        sticker = content_crop(knock_all_white(Image.open(SRC / src)))
        fitted = fit_width(sticker, width)
        canvas = blank()
        paste_bottom(canvas, fitted, 512, bottom)
        save(canvas, dest)

    print("Body (crop + place on neck)…")
    for dest, (src, width, cy) in BODIES.items():
        sticker = content_crop(knock_all_white(Image.open(SRC / src)))
        fitted = fit_width(sticker, width)
        canvas = blank()
        paste_centered(canvas, fitted, 512, cy)
        save(canvas, dest)

    print("Accessories…")
    for dest, (src, kind, width, cy) in ACCESSORIES.items():
        sticker = content_crop(knock_all_white(Image.open(SRC / src)))
        fitted = fit_width(sticker, width)
        canvas = blank()
        cx = 430 if kind == "eye" else (780 if kind == "ledge" else 512)
        paste_centered(canvas, fitted, cx, cy)
        save(canvas, dest)


def test_sheet() -> None:
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    combos = [
        ("fawn-beanie-bandana.jpg", ["background/bg-brownstone.png", "base/base-fawn-peek.png", "body/body-bandana.png", "hat/hat-beanie.png"]),
        ("cream-newsie-coffee.jpg", ["background/bg-rooftop-sunset.png", "base/base-cream-peek.png", "hat/hat-newsie.png", "accessory/acc-coffee.png"]),
        ("black-crown-chain.jpg", ["background/bg-neon-night.png", "base/base-black-peek.png", "body/body-gold-chain.png", "hat/hat-crown.png"]),
        ("fawn-hardhat-blocks.jpg", ["background/bg-stoop-day.png", "base/base-fawn-peek.png", "hat/hat-hardhat.png", "accessory/acc-blocks.png"]),
        ("black-snap-shades.jpg", ["background/bg-subway.png", "base/base-black-peek.png", "hat/hat-snapback.png", "accessory/acc-sunglasses.png"]),
        ("cream-monocle-collar.jpg", ["background/bg-chain-green.png", "base/base-cream-peek.png", "body/body-collar.png", "accessory/acc-monocle.png"]),
        ("fawn-hoodie-bone.jpg", ["background/bg-cream-brick.png", "base/base-fawn-peek.png", "body/body-hoodie.png", "accessory/acc-bone.png"]),
        ("black-bandana-shades.jpg", ["background/bg-rooftop-sunset.png", "base/base-black-peek.png", "body/body-bandana.png", "accessory/acc-sunglasses.png"]),
    ]
    for name, layers in combos:
        canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        for rel in layers:
            if rel.startswith("block/"):
                continue
            layer = Image.open(DST / rel).convert("RGBA")
            if layer.size != (SIZE, SIZE):
                layer = layer.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
            canvas = Image.alpha_composite(canvas, layer)
        out = TEST_DIR / name
        canvas.convert("RGB").save(out, "JPEG", quality=90)
        print("test", out)


if __name__ == "__main__":
    prepare()
    test_sheet()
