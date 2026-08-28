#!/usr/bin/env python3
"""Bake overlay traits so studio/generator match gallery layering.

Gallery stack (back to front):
  background → clothes → hat → pug → hat brim → wall → hanging straps →
  stoop props → paws

The pug sheets ship with a baked concrete wall. This script knocks that
wall out, extracts paws, aligns every ledge to the same rim, and places
hats/clothes at gallery scale instead of squashing them onto the wall.
"""

from __future__ import annotations

import shutil
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
TRAITS = ROOT / "public" / "traits"
SRC = ROOT / "public" / "traits-source"
GALLERY = ROOT / "public" / "gallery"
SIZE = 1024
WALL_TOP = 629
# Clothes may overlap the pug only under the chin / lower cheeks.
NECK_FRONT_Y = 520


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
    print(f"wrote {rel:36} opaque={(a[:,:,3]>20).mean()*100:5.1f}% bbox={bbox}")


def blank() -> Image.Image:
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def clear_transparent(a: np.ndarray) -> np.ndarray:
    trans = a[..., 3] == 0
    a[trans, 0] = 0
    a[trans, 1] = 0
    a[trans, 2] = 0
    return a


def neighbors8(mask: np.ndarray) -> np.ndarray:
    out = np.zeros_like(mask)
    out[1:, :] |= mask[:-1, :]
    out[:-1, :] |= mask[1:, :]
    out[:, 1:] |= mask[:, :-1]
    out[:, :-1] |= mask[:, 1:]
    out[1:, 1:] |= mask[:-1, :-1]
    out[1:, :-1] |= mask[:-1, 1:]
    out[:-1, 1:] |= mask[1:, :-1]
    out[:-1, :-1] |= mask[1:, 1:]
    return out


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
    a[a[:, :, 3] > 90, 3] = 255
    return Image.fromarray(a)


def grow(mask: np.ndarray, px: int = 3) -> np.ndarray:
    img = Image.fromarray((mask.astype(np.uint8) * 255))
    img = img.filter(ImageFilter.MaxFilter(px * 2 + 1))
    return np.array(img) > 0


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


def paste_centered(canvas: Image.Image, overlay: Image.Image, cx: float, cy: float) -> None:
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


def paste_box(
    src: Image.Image,
    box: tuple[int, int, int, int],
    anchor: str = "center",
    mode: str = "contain",
) -> Image.Image:
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
    else:
        px = x + (w - nw) // 2
        py = y + (h - nh) // 2
    canvas.paste(fitted, (px, py), fitted)
    return seal_alpha(canvas)


def fit_width(im: Image.Image, width: int, max_height: int | None = None) -> Image.Image:
    cropped = Image.fromarray(clear_transparent(arr(crop_content(im))))
    height = max(1, round(cropped.height * (width / cropped.width)))
    if max_height is not None and height > max_height:
        height = max_height
        width = max(1, round(cropped.width * (height / cropped.height)))
    return resize_rgba(cropped, (width, height))


def resize_rgba(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Premultiplied resize so transparent black cannot bleed into fabric."""
    a = arr(im).astype(np.float32)
    alpha = a[:, :, 3:4] / 255.0
    a[:, :, :3] *= alpha
    resized = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA").resize(
        size, Image.Resampling.LANCZOS
    )
    r = arr(resized).astype(np.float32)
    al = r[:, :, 3:4]
    r[:, :, :3] = np.where(al > 0, r[:, :, :3] * 255.0 / np.maximum(al, 1.0), 0)
    return Image.fromarray(np.clip(r, 0, 255).astype(np.uint8))


BASE_RELS = (
    "base/base-fawn-peek.png",
    "base/base-cream-peek.png",
    "base/base-black-peek.png",
)

BLOCK_RELS = (
    "block/block-concrete.png",
    "block/block-brownstone.png",
    "block/block-crate.png",
    "block/block-gold.png",
)

FACE_ACCESSORIES = {"sunglasses", "monocle"}
LEDGE_ACCESSORIES = {"coffee", "bone", "blocks"}


def cache_source(rel: str) -> None:
    dest = SRC / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return
    shutil.copy(TRAITS / rel, dest)
    print("cached source", rel)


def ensure_sources() -> None:
    """Keep wall-baked pugs and original ledges so this script can rerun."""
    for rel in BASE_RELS + BLOCK_RELS:
        cache_source(rel)


def sealed_source_base(rel: str) -> Image.Image:
    return seal_interior(load_src(rel))


def seal_bases() -> None:
    ensure_sources()
    for rel in BASE_RELS:
        im = sealed_source_base(rel)
        a = arr(im)
        print("sealed", rel, "forehead", tuple(int(v) for v in a[280, 512]))


def extract_paws(pug: Image.Image) -> Image.Image:
    data = arr(pug)
    rgb = data[:, :, :3].astype(np.int16)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    lum = rgb.mean(axis=2)
    alpha = data[:, :, 3] > 12
    rows = np.arange(SIZE)[:, None]
    cols = np.arange(SIZE)[None, :]
    wallish = (chroma <= 24) & (lum >= 70) & (lum <= 220) & (rows >= WALL_TOP - 6)
    seed = np.zeros((SIZE, SIZE), dtype=bool)
    seed[604 : WALL_TOP + 10, 248:412] = alpha[604 : WALL_TOP + 10, 248:412]
    seed[604 : WALL_TOP + 10, 628:800] = alpha[604 : WALL_TOP + 10, 628:800]
    seed &= ~wallish
    walk = alpha & ~wallish
    walk[:, 430:605] = False
    filled = seed.copy()
    for _ in range(16):
        nxt = neighbors8(filled) & walk & ~filled
        nxt[:598] = False
        nxt[654:] = False
        if not nxt.any():
            break
        filled |= nxt
    outline = alpha & (lum < 60) & ~wallish & (rows >= 598) & (rows <= 652)
    filled |= neighbors8(filled) & outline
    filled &= ~((cols >= 430) & (cols <= 605))
    filled[:598] = False
    filled[654:] = False
    out = np.zeros_like(data)
    out[filled] = data[filled]
    return Image.fromarray(clear_transparent(out))


def wall_mask(pug: np.ndarray) -> np.ndarray:
    rgb = pug[:, :, :3].astype(np.int16)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    lum = rgb.mean(axis=2)
    rows = np.arange(SIZE)[:, None]
    return (
        (pug[:, :, 3] > 12)
        & (rows >= WALL_TOP)
        & (chroma <= 30)
        & (lum >= 70)
        & (lum <= 210)
    )


def knock_wall_and_paws(pug: Image.Image, paws: Image.Image) -> Image.Image:
    """Remove the baked ledge only. Keep chin and chest so clothes holes stay filled."""
    data = arr(pug).copy()
    paw = arr(paws)[:, :, 3] > 12
    wall = wall_mask(data)
    data[paw | wall, 3] = 0
    # Dark grout fails the gray wall mask and otherwise leaves a thick rim.
    data[WALL_TOP:, :, 3] = 0
    return Image.fromarray(clear_transparent(data))


def extract_default_wall(pug: Image.Image, paws: Image.Image) -> Image.Image:
    data = arr(pug).copy()
    keep = wall_mask(data)
    paw = arr(paws)[:, :, 3] > 12
    keep &= ~paw
    out = np.zeros_like(data)
    out[keep] = data[keep]
    return Image.fromarray(clear_transparent(out))


def align_top(im: Image.Image, top: int) -> Image.Image:
    data = arr(im)
    ys, _xs = np.where(data[:, :, 3] > 12)
    if ys.size == 0:
        return im
    shift = top - int(ys.min())
    if shift == 0:
        return im
    canvas = blank()
    paste_centered(canvas, im, im.width / 2, im.height / 2 + shift)
    return canvas


def punch_paws(block: Image.Image, paws: Image.Image) -> Image.Image:
    return punch_mask(block, paws, dilate=6)


def punch_mask(overlay: Image.Image, mask_src: Image.Image, dilate: int = 3) -> Image.Image:
    overlay_arr = arr(overlay.convert("RGBA"))
    mask = arr(mask_src.convert("RGBA"))[:, :, 3] > 12
    for _ in range(dilate):
        mask = mask | neighbors8(mask)
    overlay_arr[mask, 3] = 0
    return Image.fromarray(clear_transparent(overlay_arr))


def split_bases() -> Image.Image:
    """Knock the baked wall out of each pug and save paws + default ledge."""
    paw_union = blank()
    for rel, color in (
        ("base/base-fawn-peek.png", "fawn"),
        ("base/base-cream-peek.png", "cream"),
        ("base/base-black-peek.png", "black"),
    ):
        pug = sealed_source_base(rel)
        paws = extract_paws(pug)
        save(f"base/front-paws-{color}.png", paws)
        paw_union = Image.alpha_composite(paw_union, paws)
        if color == "fawn":
            save("base/wall-default.png", extract_default_wall(pug, paws))
        save(rel, knock_wall_and_paws(pug, paws))
    return paw_union


def fit_blocks(paws: Image.Image) -> None:
    del paws
    for rel in BLOCK_RELS:
        save(rel, flatten_ledge(load_src(rel)))
    save("base/wall-default.png", flatten_ledge(load_trait("base/wall-default.png")))


def ledge_face_top(im: Image.Image) -> int:
    """First full-width row that is the vertical wall face, not the top-down cap."""
    a = arr(im)
    for y in range(SIZE):
        opaque = a[y, :, 3] > 20
        if opaque.mean() < 0.65:
            continue
        lum = float(a[y, opaque, :3].mean())
        if lum < 150:
            return y
    ys, _ = np.where(a[:, :, 3] > 20)
    return int(ys.min()) if ys.size else WALL_TOP


def flatten_ledge(im: Image.Image, top: int = WALL_TOP) -> Image.Image:
    """Drop the looking-down cap so paws grip a thin rim, like the gallery paintings."""
    face = ledge_face_top(im)
    data = arr(im).copy()
    if face > top:
        data[:face, :, 3] = 0
    return align_top(Image.fromarray(clear_transparent(data)), top)


def load_gallery(name: str) -> np.ndarray:
    return np.array(Image.open(GALLERY / name).convert("RGB"))


def layer_from_mask(rgb: np.ndarray, seed: np.ndarray, grow_px: int = 4) -> Image.Image:
    """Keep seed pixels plus touching ink outlines and sticker white."""
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    outline = (lum < 55) & (chroma < 50)
    white = (lum > 210) & (chroma < 40)
    filled = seed.copy()
    for _ in range(grow_px):
        filled |= neighbors8(filled) & (outline | white | seed)
    out = np.zeros((SIZE, SIZE, 4), np.uint8)
    out[filled, :3] = rgb[filled]
    out[filled, 3] = 255
    im = seal_interior(Image.fromarray(out), knock_backdrop=True)
    if (arr(im)[:, :, 3] > 20).mean() < 0.002:
        raise RuntimeError("gallery extract too thin")
    return im


def place_bottom(
    im: Image.Image,
    width: int,
    bottom_y: float,
    cx: float = 530,
    max_height: int | None = None,
) -> Image.Image:
    fitted = fit_width(im, width, max_height)
    canvas = blank()
    paste_centered(canvas, fitted, cx, bottom_y - fitted.height / 2)
    return seal_alpha(canvas)


def extract_dressed_hat(dressed_rel: str, kind: str, bottom: int) -> Image.Image:
    """Pull the on-head hat off the dressed sheet, including brim, ink, and sticker white."""
    dressed = arr(load_trait(dressed_rel))
    rgb = dressed[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    y = np.arange(SIZE)[:, None]
    x = np.arange(SIZE)[None, :]
    above = y < bottom
    alpha = dressed[:, :, 3] > 24
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)

    if kind == "beanie":
        color = (g > r + 10) & (g > b + 4) & (g > 25) & (y < 400)
    elif kind == "crown":
        gold = (r > 130) & (g > 90) & (b < 110) & (r + g > 2 * b + 10)
        gems = (r > 120) & (g < 110) & (b < 110) & (r > g + 30)
        color = gold | gems
    elif kind == "hardhat":
        # Bright dome plus the darker orange brim that sits on the forehead.
        color = (r > 120) & (g > 70) & (b < 120) & (r > b + 30) & (g > b) & (chroma > 45)
    elif kind == "newsie":
        color = (r > 70) & (g > 40) & (b < 80) & (r > b + 16) & (g > b + 8) & (r < 210) & (y < 370)
    elif kind == "snapback":
        red = (r > 130) & (g < 100) & (b < 100) & (r > g + 40)
        cream = (r > 160) & (g > 140) & (b > 120) & (r < 240) & (y < 280) & (x > 400) & (x < 640)
        panel = (r < 55) & (g < 55) & (b < 55) & (y > 140) & (y < 280) & (x > 380) & (x < 660)
        color = red | cream | panel
    else:
        raise ValueError(kind)

    seed = color & alpha & above
    filled = seed.copy()
    outline = (lum < 55) & (chroma < 50) & alpha & above
    white = (lum > 200) & (chroma < 40) & alpha & above
    for _ in range(6):
        filled |= neighbors8(filled) & (outline | white | (color & alpha & above))
    keep = grow(filled, 2) & alpha & above
    keep[bottom:] = False
    layer = np.zeros_like(dressed)
    layer[keep] = dressed[keep]
    im = seal_interior(Image.fromarray(layer), knock_backdrop=True)
    if (layer[:, :, 3] > 20).mean() < 0.005:
        raise RuntimeError(f"{kind} extract too thin")
    return im


def extract_gallery_hat(kind: str) -> Image.Image:
    """Hats from the eight paintings, isolated by color, then scaled onto this pug."""
    y = np.arange(SIZE)[:, None]
    x = np.arange(SIZE)[None, :]
    if kind == "beanie":
        rgb = load_gallery("mint-01-stoop-beanie.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        seed = (g > r + 6) & (g > b) & (g > 18) & (r < 90) & (b < 80) & (y < 520)
        return layer_from_mask(rgb, seed)
    if kind == "crown":
        rgb = load_gallery("mint-02-neon-crown.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        gold = (r > 170) & (g > 110) & (b < 140) & (r > b + 30) & (y < 420)
        gems = (r > 140) & (g < 90) & (b < 90) & (y < 420) & (x > 400) & (x < 700)
        return layer_from_mask(rgb, gold | gems)
    if kind == "newsie":
        rgb = load_gallery("mint-03-rooftop-newsie.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        seed = (r > 60) & (g > 30) & (b < 70) & (r > b + 20) & (g > b + 8) & (r < 200) & (y < 420)
        return layer_from_mask(rgb, seed)
    if kind == "hardhat":
        rgb = load_gallery("mint-04-day-hardhat.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        chroma = rgb.max(axis=2) - rgb.min(axis=2)
        seed = (r > 140) & (g > 90) & (b < 80) & (r > b + 40) & (chroma > 50) & (y < 480) & (x > 280) & (x < 820)
        return layer_from_mask(rgb, seed, grow_px=6)
    if kind == "snapback":
        rgb = load_gallery("mint-05-subway-snapback.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        red = (r > 140) & (g < 90) & (b < 90) & (r > g + 40) & (y < 420)
        cream = (r > 170) & (g > 140) & (b > 110) & (r < 245) & (y < 320) & (x > 350) & (x < 720)
        panel = (r < 50) & (g < 50) & (b < 50) & (y > 80) & (y < 320) & (x > 360) & (x < 720)
        return layer_from_mask(rgb, red | cream | panel)
    raise ValueError(kind)


def strip_pug_fur(im: Image.Image) -> Image.Image:
    """Hats extracted from dressed sheets pick up forehead fur under the brim."""
    a = arr(im).copy()
    rgb = a[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    fur = (
        (a[:, :, 3] > 20)
        & (r > 165)
        & (g > 135)
        & (b > 100)
        & (chroma < 95)
        & (b > 70)
    )
    a[fur, 3] = 0
    return Image.fromarray(clear_transparent(a))


def fit_hats() -> None:
    """Hats from the dressed fawn sheets sit on this pug; include brim and sticker white."""
    for dest, kind, bottom in [
        ("hat/hat-beanie.png", "beanie", 372),
        ("hat/hat-hardhat.png", "hardhat", 348),
        ("hat/hat-newsie.png", "newsie", 368),
        ("hat/hat-snapback.png", "snapback", 362),
    ]:
        save(dest, strip_pug_fur(extract_dressed_hat(f"dressed/fawn-{kind}.png", kind, bottom)))
    save("hat/hat-crown.png", place_bottom(load_src("hat/hat-crown.png"), 250, 310, 548, 180))


def prepare_hoodie(im: Image.Image) -> Image.Image:
    """Recolor the cowl cream. Do not fill the head hole — that peeked as blobs behind the ears."""
    a = arr(im).copy()
    rgb = a[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    opaque = a[:, :, 3] > 20
    strings = opaque & (r > g + 8) & (g > b + 4) & (chroma >= 28) & (r > 70) & (lum < 170)
    fabric = opaque & ~strings
    cream = np.array([236, 214, 186], dtype=np.float32)
    shadow = np.array([198, 170, 140], dtype=np.float32)
    t = np.clip(lum / 200.0, 0.0, 1.0).astype(np.float32)
    target = shadow[None, None, :] * (1.0 - t[:, :, None]) + cream[None, None, :] * t[:, :, None]
    a[fabric, :3] = np.clip(target[fabric], 0, 255)
    return Image.fromarray(clear_transparent(a))


def feather_front(full: Image.Image, split_y: int, fade: int = 8) -> Image.Image:
    data = arr(full).astype(np.float32)
    rows = np.arange(SIZE, dtype=np.float32)[:, None]
    data[:, :, 3] *= np.clip((rows - (split_y - fade)) / fade, 0.0, 1.0)
    return Image.fromarray(np.clip(data, 0, 255).astype(np.uint8))


def body_neck_layer(full: Image.Image, pug: Image.Image) -> Image.Image:
    """Wrap in front of the neck: keep clothes above the wall, punch the pug's face."""
    a = arr(full).copy()
    pug_a = arr(pug)[:, :, 3] > 20
    rows = np.arange(SIZE)[:, None]
    face = pug_a & (rows < NECK_FRONT_Y)
    a[face, 3] = 0
    a[WALL_TOP:, :, 3] = 0
    return Image.fromarray(clear_transparent(a))


def thicken_hoodie_neck(neck: Image.Image) -> Image.Image:
    """Close the cowl hole so the wrap is a solid band under the chin."""
    a = arr(neck).copy()
    mask = a[:, :, 3] > 20
    filled = grow(mask, 20)
    filled[:500] = mask[:500]
    filled[WALL_TOP:] = False
    filled[:, :260] = False
    filled[:, 770:] = False
    newpix = filled & (a[:, :, 3] <= 20)
    a[newpix, 0] = 236
    a[newpix, 1] = 214
    a[newpix, 2] = 186
    a[newpix, 3] = 255
    return Image.fromarray(clear_transparent(a))


def body_hang_layer(full: Image.Image, kind: str) -> Image.Image:
    """Strings, medallion, tag, and bib that hang in front of the wall."""
    a = arr(full).copy()
    rgb = a[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    rows = np.arange(SIZE)[:, None]
    alpha = a[:, :, 3] > 20
    below = np.broadcast_to(rows >= WALL_TOP - 6, alpha.shape)
    if kind == "bandana":
        # Gallery tucks the bib behind the wall; only the neck wrap should show.
        keep = np.zeros_like(alpha)
    elif kind == "hoodie":
        strings = alpha & (r > g + 6) & (g > b + 2) & (chroma >= 22) & (r > 60) & (lum < 180) & below
        keep = grow(strings, 2)
    elif kind == "gold-chain":
        # Whole necklace sits in front of the wall, like mint-02.
        gold = alpha & (r > 140) & (g > 100) & (b < 130) & (rows >= 470)
        keep = grow(gold, 2)
    elif kind == "collar":
        tag = alpha & below & (r > 140) & (g > 100) & (b < 140)
        keep = grow(tag, 3)
    else:
        keep = alpha & below
    a[~keep, 3] = 0
    return Image.fromarray(clear_transparent(a))


def fit_body(paws: Image.Image) -> None:
    pug = load_trait("base/base-fawn-peek.png")
    specs = [
        ("body/body-bandana.png", load_src("body/body-bandana.png"), 660, 552, 340, "bandana"),
        ("body/body-collar.png", load_src("body/body-collar.png"), 540, 552, 280, "collar"),
        ("body/body-hoodie.png", prepare_hoodie(load_src("body/body-hoodie.png")), 620, 548, 360, "hoodie"),
        ("body/body-gold-chain.png", load_src("body/body-gold-chain.png"), 540, 560, 400, "gold-chain"),
    ]
    for dest, src, width, cy, max_h, kind in specs:
        fitted = fit_width(src, width, max_h)
        canvas = blank()
        paste_centered(canvas, fitted, 512, cy)
        full = seal_alpha(canvas)
        back = arr(full).copy()
        if kind == "hoodie":
            # Cowl above the ears peeks as cream blobs behind the head.
            back[:500, :, 3] = 0
        save(dest, Image.fromarray(clear_transparent(back)) if kind == "hoodie" else full)
        neck = punch_mask(body_neck_layer(full, pug), paws, dilate=5)
        if kind == "hoodie":
            clipped = arr(neck)
            clipped[:500, :, 3] = 0
            neck = thicken_hoodie_neck(Image.fromarray(clear_transparent(clipped)))
        save(dest.replace(".png", "-neck.png"), neck)
        hang = punch_mask(body_hang_layer(full, kind), paws, dilate=5)
        save(dest.replace(".png", "-front.png"), hang if (arr(hang)[:, :, 3] > 20).any() else blank())


def extract_gallery_accessory(kind: str) -> Image.Image:
    y = np.arange(SIZE)[:, None]
    x = np.arange(SIZE)[None, :]
    if kind == "blocks":
        rgb = load_gallery("mint-04-day-hardhat.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        red = (r > 160) & (g < 90) & (b < 80) & (x < 480) & (y > 430) & (y < 820)
        blue = (b > 90) & (b > r + 20) & (b > g) & (x < 480) & (y > 430) & (y < 820)
        yellow = (r > 180) & (g > 140) & (b < 80) & (x < 520) & (y > 430) & (y < 820)
        return layer_from_mask(rgb, red | blue | yellow, grow_px=5)
    if kind == "coffee":
        rgb = load_gallery("mint-03-rooftop-newsie.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        cup = (r > 80) & (g > 40) & (b < 70) & (r > b + 20) & (x > 560) & (y > 480) & (y < 860)
        lid = (r > 180) & (g > 180) & (b > 170) & (x > 600) & (y > 480) & (y < 700)
        return layer_from_mask(rgb, cup | lid, grow_px=4)
    if kind == "bone":
        rgb = load_gallery("mint-07-cream-hoodie.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        bone = (r > 160) & (g > 130) & (b > 90) & (r < 250) & (x > 520) & (y > 520) & (y < 820)
        chew = (r > 90) & (r < 180) & (g > 60) & (g < 140) & (b < 100) & (x > 520) & (y > 540) & (y < 820)
        return layer_from_mask(rgb, bone | chew, grow_px=4)
    if kind == "sunglasses":
        rgb = load_gallery("mint-05-subway-snapback.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        dark = (r < 70) & (g < 70) & (b < 70) & (y > 300) & (y < 520) & (x > 280) & (x < 780)
        return layer_from_mask(rgb, dark, grow_px=3)
    if kind == "monocle":
        rgb = load_gallery("mint-06-green-monocle.png")
        r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
        gold = (r > 160) & (g > 110) & (b < 90) & (y > 280) & (y < 720) & (x < 560)
        glass = (b > g) & (g > 80) & (r < 200) & (y > 300) & (y < 520) & (x < 520)
        return layer_from_mask(rgb, gold | glass, grow_px=4)
    raise ValueError(kind)


def fit_accessories() -> None:
    """Source drawings at gallery scale, sitting on this pug's eyes / wall rim."""
    save(
        "accessory/acc-sunglasses.png",
        paste_box(load_src("accessory/acc-sunglasses.png"), (290, 355, 450, 160), "center"),
    )
    monocle = ImageOps.mirror(load_src("accessory/acc-monocle.png"))
    save(
        "accessory/acc-monocle.png",
        paste_box(monocle, (338, 358, 125, 210), "center"),
    )
    save(
        "accessory/acc-coffee.png",
        paste_box(load_src("accessory/acc-coffee.png"), (740, 470, 190, 200), "bottom"),
    )
    save(
        "accessory/acc-bone.png",
        paste_box(load_src("accessory/acc-bone.png"), (720, 515, 230, 130), "bottom"),
    )
    save(
        "accessory/acc-blocks.png",
        paste_box(load_src("accessory/acc-blocks.png"), (60, 340, 420, 305), "bottom"),
    )


def composite_stack(
    *,
    background: str,
    base: str,
    block: str | None = None,
    body: str | None = None,
    hat: str | None = None,
    accessory: str | None = None,
) -> Image.Image:
    """Gallery order: wrap behind, pug, hat, neck in front, wall, hanging bits, toys, paws."""
    color = Path(base).stem.split("-")[1]
    canvas = blank()

    def comp(rel: str | None) -> None:
        nonlocal canvas
        if not rel:
            return
        path = TRAITS / rel
        if not path.exists():
            return
        overlay = Image.open(path).convert("RGBA")
        if overlay.size != (SIZE, SIZE):
            overlay = overlay.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
        canvas = Image.alpha_composite(canvas, overlay)

    acc_id = Path(accessory).stem.replace("acc-", "") if accessory else None
    comp(background)
    comp(body)
    comp(base)
    if acc_id in FACE_ACCESSORIES:
        comp(accessory)
    comp(hat)
    if body:
        comp(body.replace(".png", "-neck.png"))
    comp(block or "base/wall-default.png")
    if body:
        comp(body.replace(".png", "-front.png"))
    if acc_id in LEDGE_ACCESSORIES:
        comp(accessory)
    comp(f"base/front-paws-{color}.png")
    return canvas


GALLERY_COMBOS = [
    ("compare-01.jpg", "mint-01-stoop-beanie.png", dict(background="background/bg-brownstone.png", base="base/base-fawn-peek.png", body="body/body-bandana.png", hat="hat/hat-beanie.png")),
    ("compare-02.jpg", "mint-02-neon-crown.png", dict(background="background/bg-neon-night.png", base="base/base-black-peek.png", body="body/body-gold-chain.png", hat="hat/hat-crown.png")),
    ("compare-03.jpg", "mint-03-rooftop-newsie.png", dict(background="background/bg-rooftop-sunset.png", base="base/base-cream-peek.png", hat="hat/hat-newsie.png", accessory="accessory/acc-coffee.png")),
    ("compare-04.jpg", "mint-04-day-hardhat.png", dict(background="background/bg-stoop-day.png", base="base/base-fawn-peek.png", hat="hat/hat-hardhat.png", accessory="accessory/acc-blocks.png")),
    ("compare-05.jpg", "mint-05-subway-snapback.png", dict(background="background/bg-subway.png", base="base/base-black-peek.png", hat="hat/hat-snapback.png", accessory="accessory/acc-sunglasses.png")),
    ("compare-06.jpg", "mint-06-green-monocle.png", dict(background="background/bg-chain-green.png", base="base/base-cream-peek.png", body="body/body-collar.png", accessory="accessory/acc-monocle.png")),
    ("compare-07.jpg", "mint-07-cream-hoodie.png", dict(background="background/bg-cream-brick.png", base="base/base-fawn-peek.png", body="body/body-hoodie.png", accessory="accessory/acc-bone.png")),
    ("compare-08.jpg", "mint-08-sunset-bandana.png", dict(background="background/bg-rooftop-sunset.png", base="base/base-black-peek.png", body="body/body-bandana.png", accessory="accessory/acc-sunglasses.png")),
]


def write_placement_tests() -> None:
    out = ROOT / "generated" / "placement-tests"
    out.mkdir(parents=True, exist_ok=True)
    combos = [
        ("stack-01-beanie-bandana.png", dict(background="background/bg-brownstone.png", base="base/base-fawn-peek.png", body="body/body-bandana.png", hat="hat/hat-beanie.png")),
        ("stack-02-crown-chain.png", dict(background="background/bg-neon-night.png", base="base/base-black-peek.png", body="body/body-gold-chain.png", hat="hat/hat-crown.png")),
        ("stack-03-newsie-coffee.png", dict(background="background/bg-rooftop-sunset.png", base="base/base-cream-peek.png", hat="hat/hat-newsie.png", accessory="accessory/acc-coffee.png")),
        ("stack-04-hardhat-blocks.png", dict(background="background/bg-stoop-day.png", base="base/base-fawn-peek.png", hat="hat/hat-hardhat.png", accessory="accessory/acc-blocks.png")),
        ("stack-05-snap-shades.png", dict(background="background/bg-subway.png", base="base/base-black-peek.png", hat="hat/hat-snapback.png", accessory="accessory/acc-sunglasses.png")),
        ("stack-06-collar-monocle.png", dict(background="background/bg-chain-green.png", base="base/base-cream-peek.png", body="body/body-collar.png", accessory="accessory/acc-monocle.png")),
        ("stack-07-hoodie-bone.png", dict(background="background/bg-cream-brick.png", base="base/base-fawn-peek.png", body="body/body-hoodie.png", accessory="accessory/acc-bone.png")),
        ("stack-08-bandana-shades.png", dict(background="background/bg-rooftop-sunset.png", base="base/base-black-peek.png", body="body/body-bandana.png", accessory="accessory/acc-sunglasses.png")),
        ("stack-gold-block.png", dict(background="background/bg-stoop-day.png", base="base/base-fawn-peek.png", block="block/block-gold.png", hat="hat/hat-beanie.png", body="body/body-hoodie.png")),
        ("stack-crate-block.png", dict(background="background/bg-brownstone.png", base="base/base-cream-peek.png", block="block/block-crate.png", hat="hat/hat-snapback.png", body="body/body-gold-chain.png")),
    ]
    for name, layers in combos:
        img = composite_stack(**layers)
        img.convert("RGB").save(out / name, "JPEG", quality=92)
        print("test", out / name)

    strips = []
    for name, gal_name, layers in GALLERY_COMBOS:
        stacked = composite_stack(**layers).convert("RGB")
        gallery = Image.open(GALLERY / gal_name).convert("RGB").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
        pair = Image.new("RGB", (SIZE * 2, SIZE))
        pair.paste(gallery, (0, 0))
        pair.paste(stacked, (SIZE, 0))
        pair.save(out / name, "JPEG", quality=90)
        a = np.array(gallery).astype(np.int16)
        b = np.array(stacked).astype(np.int16)
        mae = float(np.abs(a - b).mean())
        print(f"compare {name} mae={mae:.1f} (gallery left, stack right)")
        strips.append(pair.resize((512, 256), Image.Resampling.LANCZOS))
    if strips:
        sheet = Image.new("RGB", (512, 256 * len(strips)))
        for i, strip in enumerate(strips):
            sheet.paste(strip, (0, i * 256))
        sheet.save(out / "compare-all.jpg", "JPEG", quality=90)


def main() -> int:
    seal_bases()
    paws = split_bases()
    fit_blocks(paws)
    fit_hats()
    fit_body(paws)
    fit_accessories()
    write_placement_tests()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
