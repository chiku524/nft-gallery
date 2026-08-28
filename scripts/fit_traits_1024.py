#!/usr/bin/env python3
"""Bake overlay traits onto the 1024 canvas at gallery positions.

Hats are lifted from the dressed sheets (already sitting on the pug).
Clothes and stoop props are the original drawings, scaled into boxes
measured from the eight gallery paintings. Bases stay sealed so cream
and fawn fur is opaque. After this, the generator and studio stamp
layers 1:1 with no extra offset.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
TRAITS = ROOT / "public" / "traits"
SRC = ROOT / "public" / "traits-source"
SIZE = 1024
WALL_TOP = 629
# Eyes sit around y=360–430. Hats must stop above the pupils.
HAT_BOTTOM = 360


def load_src(rel: str) -> Image.Image:
    path = SRC / rel
    if not path.exists():
        path = TRAITS / rel
    return Image.open(path).convert("RGBA")


def load_trait(rel: str) -> Image.Image:
    return Image.open(TRAITS / rel).convert("RGBA")


def arr(im: Image.Image) -> np.ndarray:
    return np.array(im)


def save(rel: str, im: Image.Image) -> None:
    path = TRAITS / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)
    a = arr(im)
    ys, xs = np.where(a[:, :, 3] > 20)
    bbox = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())) if xs.size else None
    print(f"wrote {rel:32} opaque={(a[:,:,3]>20).mean()*100:5.1f}% bbox={bbox}")


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def flood_from_edges(open_mask: np.ndarray) -> np.ndarray:
    h, w = open_mask.shape
    visited = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()

    def push(y: int, x: int) -> None:
        if 0 <= y < h and 0 <= x < w and open_mask[y, x] and not visited[y, x]:
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
        push(y - 1, x)
        push(y + 1, x)
        push(y, x - 1)
        push(y, x + 1)
    return visited


def seal_interior(im: Image.Image, hole_thresh: int = 96, knock_backdrop: bool = False) -> Image.Image:
    a = arr(im).copy()
    alpha = a[:, :, 3]
    openp = alpha < hole_thresh
    backdrop = flood_from_edges(openp)
    enclosed = openp & ~backdrop
    interior = ~backdrop
    near_bg = np.array(Image.fromarray((backdrop.astype(np.uint8) * 255)).filter(ImageFilter.MaxFilter(3))) > 0
    body = interior & ~near_bg
    if knock_backdrop:
        a[backdrop & openp, 3] = 0
    a[enclosed, 3] = 255
    mid = body & (a[:, :, 3] > 0) & (a[:, :, 3] < 255)
    a[mid, 3] = 255
    return Image.fromarray(a)


def seal_alpha(im: Image.Image) -> Image.Image:
    a = arr(im).astype(np.uint8)
    alpha = a[:, :, 3]
    solid = alpha > 90
    a[solid, 3] = 255
    return Image.fromarray(a)


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
    x1 = min(a.shape[1], x1 + pad)
    y1 = min(a.shape[0], y1 + pad)
    return Image.fromarray(a[y0:y1, x0:x1])


def paste_box(
    src: Image.Image,
    box: tuple[int, int, int, int],
    anchor: str = "center",
    mode: str = "contain",
) -> Image.Image:
    """Scale `src` to fit inside (x, y, w, h) and paste onto a 1024 canvas."""
    x, y, w, h = box
    cropped = crop_content(src)
    if mode == "fill":
        fitted = cropped.resize((w, h), Image.Resampling.LANCZOS)
        nw, nh = w, h
    else:
        scale = min(w / cropped.width, h / cropped.height)
        nw = max(1, int(cropped.width * scale))
        nh = max(1, int(cropped.height * scale))
        fitted = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = blank()
    if anchor == "bottom":
        px = x + (w - nw) // 2
        py = y + h - nh
    elif anchor == "top":
        px = x + (w - nw) // 2
        py = y
    elif anchor == "bottom-left":
        px = x
        py = y + h - nh
    else:
        px = x + (w - nw) // 2
        py = y + (h - nh) // 2
    canvas.paste(fitted, (px, py), fitted)
    return seal_alpha(canvas)


def extract_dressed_hat(dressed_rel: str, kind: str) -> Image.Image:
    dressed = arr(load_trait(dressed_rel))
    rgb = dressed[:, :, :3].astype(np.int16)
    alpha = dressed[:, :, 3] > 24
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    y = np.arange(SIZE)[:, None]
    above_eyes = y < HAT_BOTTOM

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

    mask = alpha & above_eyes & color
    mask_img = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))
    mask = np.array(mask_img) > 0
    mask[HAT_BOTTOM:] = False
    layer = np.zeros_like(dressed)
    layer[mask] = dressed[mask]
    im = seal_interior(Image.fromarray(layer), knock_backdrop=True)
    if (layer[:, :, 3] > 20).mean() < 0.005:
        raise RuntimeError(f"{kind} extract too thin")
    return im


def seal_bases() -> None:
    for rel in (
        "base/base-fawn-peek.png",
        "base/base-cream-peek.png",
        "base/base-black-peek.png",
    ):
        src = TRAITS / rel
        im = seal_interior(Image.open(src).convert("RGBA"))
        im.save(src)
        a = arr(im)
        print("sealed", rel, "forehead", tuple(int(v) for v in a[280, 512]))


def fit_hats() -> None:
    for dest, src, kind in [
        ("hat/hat-beanie.png", "dressed/fawn-beanie.png", "beanie"),
        ("hat/hat-hardhat.png", "dressed/fawn-hardhat.png", "hardhat"),
        ("hat/hat-newsie.png", "dressed/fawn-newsie.png", "newsie"),
        ("hat/hat-crown.png", "dressed/fawn-crown.png", "crown"),
        ("hat/hat-snapback.png", "dressed/fawn-snapback.png", "snapback"),
    ]:
        save(dest, extract_dressed_hat(src, kind))


def knock_out_hoodie_fill(im: Image.Image) -> Image.Image:
    """Drop the cream neck lining so the pug's chin shows through the hood."""
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


def recolor_hoodie_cream(im: Image.Image) -> Image.Image:
    """Gallery mint-07 paints a cream hoodie, not the charcoal source sheet."""
    a = arr(im).astype(np.float32)
    rgb = a[:, :, :3]
    alpha = a[:, :, 3]
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    fabric = (alpha > 20) & (lum < 150) & (chroma < 70)
    cream = np.array([236, 214, 186], dtype=np.float32)
    shadow = np.array([196, 168, 136], dtype=np.float32)
    t = np.clip(lum / 140.0, 0.0, 1.0)
    target = shadow[None, None, :] * (1.0 - t[:, :, None]) + cream[None, None, :] * t[:, :, None]
    rgb[fabric] = target[fabric]
    a[:, :, :3] = rgb
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def fit_body() -> None:
    # Boxes measured from the gallery paintings (mint-01 bandana, mint-06 collar,
    # mint-07 hoodie, mint-02 chain). Fill-mode squashes the tall source drawings
    # into a chest band the way the gallery paints them.
    save(
        "body/body-bandana.png",
        paste_box(load_src("body/body-bandana.png"), (339, 552, 460, 88), "bottom", mode="fill"),
    )
    save(
        "body/body-collar.png",
        paste_box(load_src("body/body-collar.png"), (329, 530, 346, 110), "bottom", mode="fill"),
    )
    hoodie = knock_out_hoodie_fill(load_src("body/body-hoodie.png"))
    hoodie = recolor_hoodie_cream(hoodie)
    save(
        "body/body-hoodie.png",
        paste_box(hoodie, (220, 540, 580, 220), "top"),
    )
    save(
        "body/body-gold-chain.png",
        paste_box(load_src("body/body-gold-chain.png"), (328, 575, 370, 120), "bottom", mode="fill"),
    )


def fit_accessories() -> None:
    save(
        "accessory/acc-sunglasses.png",
        paste_box(load_src("accessory/acc-sunglasses.png"), (300, 330, 420, 150), "center"),
    )
    monocle = ImageOps.mirror(load_src("accessory/acc-monocle.png"))
    save(
        "accessory/acc-monocle.png",
        paste_box(monocle, (250, 300, 250, 310), "center"),
    )
    save(
        "accessory/acc-coffee.png",
        paste_box(load_src("accessory/acc-coffee.png"), (640, 470, 170, 170), "bottom"),
    )
    save(
        "accessory/acc-bone.png",
        paste_box(load_src("accessory/acc-bone.png"), (640, 500, 220, 140), "bottom"),
    )
    save(
        "accessory/acc-blocks.png",
        paste_box(load_src("accessory/acc-blocks.png"), (150, 450, 230, 180), "bottom"),
    )


def main() -> int:
    seal_bases()
    fit_hats()
    fit_body()
    fit_accessories()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
