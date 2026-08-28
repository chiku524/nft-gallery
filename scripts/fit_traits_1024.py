#!/usr/bin/env python3
"""Bake every overlay trait onto a 1024×1024 canvas at gallery positions.

Backgrounds, bases, and blocks are already full-frame. Hats are taken from
the dressed sheets so they sit on the pug like the mint paintings. Clothes
and accessories are cropped and placed on the neck, face, or stoop. After
this, the generator and studio stamp layers 1:1 with no scale or offset.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
TRAITS = ROOT / "public" / "traits"
SRC = ROOT / "public" / "traits-source"
SIZE = 1024
WALL_TOP = 629
HEAD_CX = 512


def load(rel: str) -> Image.Image:
    path = SRC / rel if (SRC / rel).exists() else TRAITS / rel
    return Image.open(path).convert("RGBA")


def arr(im: Image.Image) -> np.ndarray:
    return np.array(im)


def save(rel: str, im: Image.Image) -> None:
    path = TRAITS / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)
    print("wrote", rel, im.size)


def content_bbox(a: np.ndarray, thresh: int = 18) -> tuple[int, int, int, int]:
    ys, xs = np.where(a[:, :, 3] > thresh)
    if xs.size == 0:
        raise ValueError("empty layer")
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def crop_content(im: Image.Image, pad: int = 2) -> Image.Image:
    a = arr(im)
    x0, y0, x1, y1 = content_bbox(a)
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(SIZE, x1 + pad)
    y1 = min(SIZE, y1 + pad)
    return Image.fromarray(a[y0:y1, x0:x1])


def seal_alpha(im: Image.Image) -> Image.Image:
    """Keep edge AA, but make interior coverage solid so hats are not ghostly."""
    a = arr(im).astype(np.uint8)
    alpha = a[:, :, 3]
    solid = alpha > 90
    a[solid, 3] = 255
    return Image.fromarray(a)


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def paste_box(src: Image.Image, box: tuple[int, int, int, int], anchor: str = "center") -> Image.Image:
    """Scale `src` to fit inside (x, y, w, h) and paste onto a 1024 canvas."""
    x, y, w, h = box
    cropped = crop_content(src)
    scale = min(w / cropped.width, h / cropped.height)
    nw = max(1, int(cropped.width * scale))
    nh = max(1, int(cropped.height * scale))
    fitted = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = blank()
    if anchor == "bottom":
        px = x + (w - nw) // 2
        py = y + h - nh
    elif anchor == "bottom-left":
        px = x
        py = y + h - nh
    elif anchor == "bottom-right":
        px = x + w - nw
        py = y + h - nh
    else:
        px = x + (w - nw) // 2
        py = y + (h - nh) // 2
    canvas.paste(fitted, (px, py), fitted)
    return seal_alpha(canvas)


def extract_dressed_hat(dressed_rel: str, kind: str) -> Image.Image:
    dressed = arr(load(dressed_rel))
    rgb = dressed[:, :, :3].astype(np.int16)
    alpha = dressed[:, :, 3] > 24
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    y = np.arange(SIZE)[:, None]
    above_wall = y < WALL_TOP - 8

    if kind == "beanie":
        color = (g > r + 18) & (g > b + 12) & (g > 40)
    elif kind == "crown":
        color = (r > 140) & (g > 110) & (b < 90) & (r + g > 2 * b + 40)
    elif kind == "hardhat":
        color = (r > 160) & (g > 140) & (b < 80)
    elif kind == "newsie":
        color = (r > 70) & (g > 40) & (b < 70) & (r > b + 20) & (g > b + 10) & (r < 200)
    elif kind == "snapback":
        color = ((r > 140) & (g < 90) & (b < 90)) | ((r > 160) & (g > 140) & (b > 120) & (r < 240))
    else:
        raise ValueError(kind)

    mask = alpha & above_wall & color
    # Grow slightly so the black outline comes along.
    mask_img = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))
    mask = np.array(mask_img) > 0
    layer = np.zeros_like(dressed)
    layer[mask] = dressed[mask]
    im = seal_alpha(Image.fromarray(layer))
    # If the extract is too thin, fall back to a fitted crop of the hat sheet.
    if (layer[:, :, 3] > 20).mean() < 0.02:
        raise RuntimeError(f"{kind} extract too thin")
    return im


def fit_hats() -> None:
    # Dressed sheets already have the beanie / newsie / hard hat sitting on the pug.
    for dest, src, kind in [
        ("hat/hat-beanie.png", "dressed/fawn-beanie.png", "beanie"),
        ("hat/hat-hardhat.png", "dressed/fawn-hardhat.png", "hardhat"),
        ("hat/hat-newsie.png", "dressed/fawn-newsie.png", "newsie"),
    ]:
        save(dest, extract_dressed_hat(src, kind))

    # Crown and snapback sheets are hat-only drawings; sit them on the skull,
    # between the ears — not stretched over the eyes.
    save("hat/hat-crown.png", paste_box(load("hat/hat-crown.png"), (330, 95, 360, 220), "bottom"))
    save("hat/hat-snapback.png", paste_box(load("hat/hat-snapback.png"), (250, 70, 520, 300), "bottom"))


def knock_out_hoodie_fill(im: Image.Image) -> Image.Image:
    """The hoodie sheet fills the neck hole with cream lining — drop that so the pug shows through."""
    a = arr(im)
    rgb = a[:, :, :3].astype(np.int16)
    alpha = a[:, :, 3]
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    lining = (alpha > 20) & (r > 140) & (g > 110) & (b > 70) & (r > b)
    fabric = (alpha > 20) & ~lining
    rim = np.array(Image.fromarray((fabric * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))) > 0
    keep = fabric | (lining & rim)
    a[~keep, 3] = 0
    return Image.fromarray(a)


def fit_body() -> None:
    # Neck band sits on the stoop line, under the chin, not over the eyes.
    neck = (210, 400, 600, 230)
    save("body/body-bandana.png", paste_box(load("body/body-bandana.png"), neck, "bottom"))
    save("body/body-collar.png", paste_box(load("body/body-collar.png"), (230, 410, 560, 220), "bottom"))
    hoodie = knock_out_hoodie_fill(load("body/body-hoodie.png"))
    save("body/body-hoodie.png", paste_box(hoodie, (200, 430, 620, 220), "bottom"))
    save("body/body-gold-chain.png", paste_box(load("body/body-gold-chain.png"), (250, 430, 520, 230), "bottom"))


def fit_accessories() -> None:
    # Face wear covers the eyes the way mint-05 / mint-06 do.
    save(
        "accessory/acc-sunglasses.png",
        paste_box(load("accessory/acc-sunglasses.png"), (270, 310, 480, 200), "center"),
    )
    save(
        "accessory/acc-monocle.png",
        paste_box(load("accessory/acc-monocle.png"), (300, 300, 280, 280), "center"),
    )
    # Stoop toys sit on the wall: coffee/bone to the right, blocks to the left.
    ledge_right = (620, 470, 210, 170)
    ledge_left = (170, 470, 220, 170)
    save("accessory/acc-coffee.png", paste_box(load("accessory/acc-coffee.png"), ledge_right, "bottom"))
    save("accessory/acc-bone.png", paste_box(load("accessory/acc-bone.png"), ledge_right, "bottom"))
    save("accessory/acc-blocks.png", paste_box(load("accessory/acc-blocks.png"), ledge_left, "bottom"))


def main() -> int:
    fit_hats()
    fit_body()
    fit_accessories()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
