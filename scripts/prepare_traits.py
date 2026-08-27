#!/usr/bin/env python3
"""Rebuild trait PNGs with clean alpha and pug-relative placement.

Bases: flood-fill white from the edges only so cream/fawn fur stays opaque,
then strip the light anti-aliased halo that sits outside the black outline.
Hats, body, accessories: knock out all white, defringe, crop to content, and
paste onto a 1024 canvas at pug landmarks so the studio and the 10k generator
stack layers 1:1.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = Path("/opt/cursor/artifacts/assets")
DST = ROOT / "public" / "traits"
SIZE = 1024
TEST_DIR = ROOT / "generated" / "placement-tests"

# Pug landmarks on the 1024 canvas (measured from the processed bases):
#   head silhouette top ≈ 197
#   eyes ≈ 360–430 (cy ≈ 398)
#   chin on the ledge ≈ 620–629
#   wall top rim ≈ 630–639
HEAD_TOP = 197
EYE_CY = 398
WALL_TOP = 629


def _neighbors4(mask: np.ndarray) -> np.ndarray:
    out = np.zeros_like(mask)
    out[1:, :] |= mask[:-1, :]
    out[:-1, :] |= mask[1:, :]
    out[:, 1:] |= mask[:, :-1]
    out[:, :-1] |= mask[:, 1:]
    return out


def _neighbors8(mask: np.ndarray) -> np.ndarray:
    out = _neighbors4(mask)
    out[1:, 1:] |= mask[:-1, :-1]
    out[1:, :-1] |= mask[:-1, 1:]
    out[:-1, 1:] |= mask[1:, :-1]
    out[:-1, :-1] |= mask[1:, 1:]
    return out


def clear_transparent(arr: np.ndarray) -> np.ndarray:
    """Zero RGB on transparent pixels so later resizes cannot bleed white."""
    trans = arr[..., 3] == 0
    arr[trans, 0] = 0
    arr[trans, 1] = 0
    arr[trans, 2] = 0
    return arr


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

    return Image.fromarray(clear_transparent(arr), "RGBA")


def knock_all_white(im: Image.Image, thresh: int = 246) -> Image.Image:
    """Transparent for every near-white pixel (opens bandana/chain holes)."""
    arr = np.array(im.convert("RGBA"))
    white = arr[..., :3].min(axis=2) >= thresh
    arr[..., 3] = np.where(white, 0, arr[..., 3]).astype(np.uint8)
    return Image.fromarray(clear_transparent(arr), "RGBA")


def defringe(
    im: Image.Image,
    lum_cut: int = 150,
    chroma_cut: int = 36,
    passes: int = 3,
    connectivity: int = 4,
) -> Image.Image:
    """Remove the light halo left by knocking a white backdrop.

    Two artifacts show up at the silhouette:

      1. Leftover near-white pixels (lum >= lum_cut) — fully transparent.
      2. Gray anti-aliasing that was baked against white (lum 50–150,
         full opacity). Those look like a pale ring on any dark or
         colored background. Recover coverage as if the source was a
         black outline over white: alpha = 1 - lum/255, RGB = black.

    Only near-neutral pixels that touch transparency are touched, so
    cream fur, gold tags, eye highlights, and snapback panels stay put.
    """
    neigh = _neighbors8 if connectivity == 8 else _neighbors4
    arr = np.array(im.convert("RGBA"))
    for _ in range(passes):
        rgb = arr[..., :3].astype(np.int16)
        alpha = arr[..., 3]
        lum = rgb.mean(axis=2)
        chroma = rgb.max(axis=2) - rgb.min(axis=2)
        opaque = alpha > 8
        trans = ~opaque
        edge = opaque & neigh(trans) & (chroma <= chroma_cut)
        if not edge.any():
            break
        white = edge & (lum >= lum_cut)
        aa = edge & (lum >= 48) & (lum < lum_cut)
        if not white.any() and not aa.any():
            break
        arr[white, 3] = 0
        if aa.any():
            coverage = np.clip(1.0 - lum[aa] / 255.0, 0.0, 1.0)
            arr[aa, 0] = 0
            arr[aa, 1] = 0
            arr[aa, 2] = 0
            arr[aa, 3] = np.clip(coverage * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(clear_transparent(arr), "RGBA")


# Bases: aggressive. Overlays: conservative so cream hoodies / gold stay intact.
DEFRINGE_BASE = dict(lum_cut=110, chroma_cut=40, passes=6, connectivity=8)
DEFRINGE_OVERLAY = dict(lum_cut=180, chroma_cut=16, passes=3, connectivity=4)


def content_crop(im: Image.Image, pad: int = 1) -> Image.Image:
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
    resized = im.resize((width, height), Image.Resampling.LANCZOS)
    # LANCZOS samples transparent neighbors and can reintroduce a light fringe.
    return defringe(resized, **DEFRINGE_OVERLAY)


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


def fringe_count(im: Image.Image) -> int:
    arr = np.array(im.convert("RGBA"))
    rgb = arr[..., :3].astype(np.int16)
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    opaque = arr[..., 3] > 8
    edge = opaque & _neighbors4(~opaque) & (chroma <= 36) & (lum >= 80)
    return int(edge.sum())


def save(im: Image.Image, rel: str) -> None:
    path = DST / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)
    arr = np.array(im)
    print(
        f"  {rel} opaque={((arr[..., 3] > 12).mean()*100):.1f}% "
        f"halo={fringe_count(im)}"
    )


def sticker_from(src_name: str) -> Image.Image:
    return content_crop(defringe(knock_all_white(Image.open(SRC / src_name)), **DEFRINGE_OVERLAY))


# Hats sit on the crown: brim aligned to the forehead, just above the eyes.
HATS = {
    "hat/hat-beanie.png": ("hat-only-beanie.png", 300, 358),
    "hat/hat-crown.png": ("hat-only-crown.png", 224, 348),
    "hat/hat-snapback.png": ("hat-only-snapback.png", 310, 374),
    "hat/hat-newsie.png": ("hat-only-newsie.png", 300, 362),
    "hat/hat-hardhat.png": ("hat-only-hardhat.png", 296, 364),
}

# Neck items tuck under the chin and rest on the wall line.
BODIES = {
    "body/body-bandana.png": ("body-bandana.png", 236, 636),
    "body/body-collar.png": ("body-collar.png", 228, 642),
    "body/body-hoodie.png": ("body-hoodie.png", 300, 640),
    "body/body-gold-chain.png": ("body-gold-chain.png", 214, 636),
}

ACCESSORIES = {
    "accessory/acc-sunglasses.png": ("acc-sunglasses.png", "eyes", 248, 408),
    "accessory/acc-monocle.png": ("acc-monocle.png", "eye", 118, 392),
    "accessory/acc-coffee.png": ("acc-coffee.png", "ledge", 128, 622),
    "accessory/acc-bone.png": ("acc-bone.png", "ledge", 170, 618),
    "accessory/acc-blocks.png": ("acc-blocks.png", "ledge", 168, 624),
}

LEDGE_X = 800

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
    print("Bases (edge flood-fill + defringe)…")
    boosts = {
        "base/base-fawn-peek.png": ((214, 168, 128), 0.22),
        "base/base-cream-peek.png": ((228, 186, 142), 0.38),
        "base/base-black-peek.png": None,
    }
    for dest, src in BASES.items():
        prepared = defringe(flood_white(Image.open(SRC / src)), **DEFRINGE_BASE)
        extra = boosts[dest]
        if extra:
            prepared = boost_fill(prepared, extra[0], extra[1])
        save(prepared, dest)

    print("Blocks (edge flood-fill + defringe)…")
    for dest, src in BLOCKS.items():
        save(defringe(flood_white(Image.open(SRC / src)), **DEFRINGE_BASE), dest)

    print("Hats (crop + place on crown)…")
    for dest, (src, width, bottom) in HATS.items():
        fitted = fit_width(sticker_from(src), width)
        canvas = blank()
        paste_bottom(canvas, fitted, 512, bottom)
        save(canvas, dest)

    print("Body (crop + place on neck)…")
    for dest, (src, width, cy) in BODIES.items():
        fitted = fit_width(sticker_from(src), width)
        canvas = blank()
        paste_centered(canvas, fitted, 512, cy)
        save(canvas, dest)

    print("Accessories…")
    for dest, (src, kind, width, cy) in ACCESSORIES.items():
        fitted = fit_width(sticker_from(src), width)
        canvas = blank()
        if kind == "eye":
            cx = 428
        elif kind == "ledge":
            cx = LEDGE_X
        else:
            cx = 512
        paste_centered(canvas, fitted, cx, cy)
        save(canvas, dest)


def composite(layers: list[str], bg: tuple[int, int, int] | None = None) -> Image.Image:
    if bg is None:
        canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    else:
        canvas = Image.new("RGBA", (SIZE, SIZE), (*bg, 255))
    for rel in layers:
        if rel.startswith("block/"):
            continue
        layer = Image.open(DST / rel).convert("RGBA")
        if layer.size != (SIZE, SIZE):
            layer = layer.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
        canvas = Image.alpha_composite(canvas, layer)
    return canvas


def _font(size: int) -> ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def labeled_tile(image: Image.Image, label: str, tile: int = 320) -> Image.Image:
    thumb = image.resize((tile, tile), Image.Resampling.LANCZOS).convert("RGB")
    draw = ImageDraw.Draw(thumb)
    font = _font(16)
    draw.rectangle((0, tile - 28, tile, tile), fill=(8, 8, 8))
    draw.text((8, tile - 24), label, fill=(255, 255, 255), font=font)
    return thumb


def grid(tiles: list[Image.Image], columns: int, path: Path) -> None:
    if not tiles:
        return
    tile_w, tile_h = tiles[0].size
    rows = (len(tiles) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * tile_w, rows * tile_h), (12, 12, 12))
    for i, tile in enumerate(tiles):
        x = (i % columns) * tile_w
        y = (i // columns) * tile_h
        sheet.paste(tile, (x, y))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, "PNG")
    print("sheet", path)


def test_sheet() -> None:
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    teal = (18, 78, 92)
    crimson = (140, 28, 48)

    tiles: list[Image.Image] = []
    for name, rel in [
        ("fawn / teal", "base/base-fawn-peek.png"),
        ("cream / teal", "base/base-cream-peek.png"),
        ("black / teal", "base/base-black-peek.png"),
        ("fawn / crimson", "base/base-fawn-peek.png"),
        ("cream / crimson", "base/base-cream-peek.png"),
        ("black / crimson", "base/base-black-peek.png"),
    ]:
        bg = teal if "teal" in name else crimson
        tiles.append(labeled_tile(composite([rel], bg), name))
    grid(tiles, 3, TEST_DIR / "halo-check.png")

    hat_tiles = []
    for dest in HATS:
        label = Path(dest).stem
        img = composite(
            ["background/bg-stoop-day.png", "base/base-fawn-peek.png", dest]
        )
        hat_tiles.append(labeled_tile(img, label))
        img.convert("RGB").save(TEST_DIR / f"{label}.jpg", "JPEG", quality=90)
    grid(hat_tiles, 5, TEST_DIR / "hats.png")

    body_tiles = []
    for dest in BODIES:
        label = Path(dest).stem
        img = composite(
            ["background/bg-brownstone.png", "base/base-fawn-peek.png", dest]
        )
        body_tiles.append(labeled_tile(img, label))
        img.convert("RGB").save(TEST_DIR / f"{label}.jpg", "JPEG", quality=90)
    grid(body_tiles, 4, TEST_DIR / "bodies.png")

    acc_tiles = []
    for dest in ACCESSORIES:
        label = Path(dest).stem
        img = composite(
            ["background/bg-rooftop-sunset.png", "base/base-cream-peek.png", dest]
        )
        acc_tiles.append(labeled_tile(img, label))
        img.convert("RGB").save(TEST_DIR / f"{label}.jpg", "JPEG", quality=90)
    grid(acc_tiles, 5, TEST_DIR / "accessories.png")

    combos = [
        ("fawn-beanie-bandana.jpg", ["background/bg-brownstone.png", "base/base-fawn-peek.png", "body/body-bandana.png", "hat/hat-beanie.png"]),
        ("cream-newsie-coffee.jpg", ["background/bg-rooftop-sunset.png", "base/base-cream-peek.png", "hat/hat-newsie.png", "accessory/acc-coffee.png"]),
        ("black-crown-chain.jpg", ["background/bg-neon-night.png", "base/base-black-peek.png", "body/body-gold-chain.png", "hat/hat-crown.png"]),
        ("fawn-hardhat-blocks.jpg", ["background/bg-stoop-day.png", "base/base-fawn-peek.png", "hat/hat-hardhat.png", "accessory/acc-blocks.png"]),
        ("black-snap-shades.jpg", ["background/bg-subway.png", "base/base-black-peek.png", "hat/hat-snapback.png", "accessory/acc-sunglasses.png"]),
        ("cream-monocle-collar.jpg", ["background/bg-chain-green.png", "base/base-cream-peek.png", "body/body-collar.png", "accessory/acc-monocle.png"]),
        ("fawn-hoodie-bone.jpg", ["background/bg-cream-brick.png", "base/base-fawn-peek.png", "body/body-hoodie.png", "accessory/acc-bone.png"]),
        ("black-bandana-shades.jpg", ["background/bg-rooftop-sunset.png", "base/base-black-peek.png", "body/body-bandana.png", "accessory/acc-sunglasses.png"]),
        ("fawn-snap-hoodie-coffee.jpg", ["background/bg-brownstone.png", "base/base-fawn-peek.png", "body/body-hoodie.png", "hat/hat-snapback.png", "accessory/acc-coffee.png"]),
        ("cream-beanie-collar-shades.jpg", ["background/bg-stoop-day.png", "base/base-cream-peek.png", "body/body-collar.png", "hat/hat-beanie.png", "accessory/acc-sunglasses.png"]),
    ]
    stack_tiles = []
    for name, layers in combos:
        canvas = composite(layers)
        out = TEST_DIR / name
        canvas.convert("RGB").save(out, "JPEG", quality=90)
        stack_tiles.append(labeled_tile(canvas, name.replace(".jpg", "")))
        print("test", out)
    grid(stack_tiles, 5, TEST_DIR / "stacks.png")


if __name__ == "__main__":
    prepare()
    test_sheet()
