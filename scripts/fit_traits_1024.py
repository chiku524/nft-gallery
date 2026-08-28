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
SIZE = 1024
WALL_TOP = 629


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
    for rel in BLOCK_RELS:
        aligned = align_top(load_src(rel), WALL_TOP)
        save(rel, aligned)
    save("base/wall-default.png", load_trait("base/wall-default.png"))


def extract_dressed_hat(dressed_rel: str, kind: str, bottom: int) -> Image.Image:
    """Pull the on-head hat off the dressed sheet, including outlines and gems."""
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
        color = (g > r + 12) & (g > b + 6) & (g > 30) & (y < 380)
    elif kind == "crown":
        gold = (r > 130) & (g > 90) & (b < 110) & (r + g > 2 * b + 10)
        gems = (r > 120) & (g < 110) & (b < 110) & (r > g + 30)
        color = gold | gems
    elif kind == "hardhat":
        color = (r > 150) & (g > 130) & (b < 100)
    elif kind == "newsie":
        color = (r > 70) & (g > 40) & (b < 80) & (r > b + 16) & (g > b + 8) & (r < 210) & (y < 355)
    elif kind == "snapback":
        red = (r > 130) & (g < 100) & (b < 100) & (r > g + 40)
        cream = (r > 160) & (g > 140) & (b > 120) & (r < 240) & (y < 270) & (x > 400) & (x < 640)
        panel = (r < 55) & (g < 55) & (b < 55) & (y > 140) & (y < 270) & (x > 380) & (x < 660)
        color = red | cream | panel
    else:
        raise ValueError(kind)

    seed = color & alpha & above
    # Only the outlines that actually touch the hat, not the pug's head contour.
    filled = seed.copy()
    outline = (lum < 48) & (chroma < 40) & alpha & above
    for _ in range(3):
        filled |= neighbors8(filled) & outline
    keep = grow(filled, 1) & alpha & above
    keep[bottom:] = False
    keep[390:] = False
    layer = np.zeros_like(dressed)
    layer[keep] = dressed[keep]
    im = seal_interior(Image.fromarray(layer), knock_backdrop=True)
    if (layer[:, :, 3] > 20).mean() < 0.005:
        raise RuntimeError(f"{kind} extract too thin")
    return im


def place_source_hat(src_rel: str, width: int, bottom_y: int, cx: float = 512) -> Image.Image:
    fitted = fit_width(load_src(src_rel), width)
    canvas = blank()
    paste_centered(canvas, fitted, cx, bottom_y - fitted.height / 2)
    return seal_alpha(canvas)


def fit_hats() -> None:
    for dest, src, kind, bottom in [
        ("hat/hat-beanie.png", "dressed/fawn-beanie.png", "beanie", 365),
        ("hat/hat-hardhat.png", "dressed/fawn-hardhat.png", "hardhat", 330),
        ("hat/hat-newsie.png", "dressed/fawn-newsie.png", "newsie", 360),
        ("hat/hat-snapback.png", "dressed/fawn-snapback.png", "snapback", 365),
    ]:
        save(dest, extract_dressed_hat(src, kind, bottom))
    # Source crown is a complete drawing; the dressed extract leaves head scribbles.
    save("hat/hat-crown.png", place_source_hat("hat/hat-crown.png", 220, 296, 542))


def prepare_hoodie(im: Image.Image) -> Image.Image:
    """Fill the cowl with gallery cream; keep brown drawstrings and the outer ink."""
    a = arr(im).copy()
    alpha = a[:, :, 3]
    openp = alpha < 96
    backdrop = flood_from_edges(openp)
    enclosed = openp & ~backdrop
    a[enclosed, 0] = 210
    a[enclosed, 1] = 185
    a[enclosed, 2] = 155
    a[enclosed, 3] = 255

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
    silhouette = opaque & neighbors8(backdrop)
    a[silhouette & (lum < 48) & ~strings, :3] = (18, 14, 12)
    return Image.fromarray(clear_transparent(a))


def feather_front(full: Image.Image, split_y: int, fade: int = 8) -> Image.Image:
    data = arr(full).astype(np.float32)
    rows = np.arange(SIZE, dtype=np.float32)[:, None]
    data[:, :, 3] *= np.clip((rows - (split_y - fade)) / fade, 0.0, 1.0)
    return Image.fromarray(np.clip(data, 0, 255).astype(np.uint8))


def body_front_layer(full: Image.Image, kind: str, split_y: int) -> Image.Image:
    """Only the bits that hang over the wall: strings, medallion, collar tag."""
    a = arr(full).copy()
    rgb = a[:, :, :3].astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    y = np.arange(SIZE)[:, None]
    x = np.arange(SIZE)[None, :]
    alpha = a[:, :, 3] > 20
    if kind == "bandana":
        a[:, :, 3] = 0
    elif kind == "hoodie":
        # Recolor turns the cords cream with the cowl; a color mask then
        # stamps a fabric rectangle on the wall. Skip the front layer.
        a[:, :, 3] = 0
    elif kind == "gold-chain":
        gold = alpha & (r > 140) & (g > 100) & (b < 130) & (y >= split_y)
        keep = grow(gold, 2)
        a[~keep, 3] = 0
    elif kind == "collar":
        tag = alpha & (y >= split_y) & (r > 150) & (g > 110) & (b < 120)
        keep = grow(tag, 3)
        a[~keep, 3] = 0
    else:
        a[:, :, 3] = 0
    del lum
    return Image.fromarray(clear_transparent(a))


def fit_body(paws: Image.Image) -> None:
    del paws
    # Wider than the head so the wrap peeks beside the cheeks, not only under the chin.
    # (dest, source, width, center-y, max-height, front-split-y, kind)
    specs = [
        ("body/body-bandana.png", load_src("body/body-bandana.png"), 640, 548, 340, 612, "bandana"),
        ("body/body-collar.png", load_src("body/body-collar.png"), 520, 560, 300, 618, "collar"),
        ("body/body-hoodie.png", prepare_hoodie(load_src("body/body-hoodie.png")), 580, 548, 340, 612, "hoodie"),
        ("body/body-gold-chain.png", load_src("body/body-gold-chain.png"), 500, 545, 420, 615, "gold-chain"),
    ]
    for dest, src, width, cy, max_h, split_y, kind in specs:
        fitted = fit_width(src, width, max_h)
        canvas = blank()
        paste_centered(canvas, fitted, 512, cy)
        full = seal_alpha(canvas)
        save(dest, full)
        front = body_front_layer(full, kind, split_y)
        if (arr(front)[:, :, 3] > 20).any():
            save(dest.replace(".png", "-front.png"), front)
        else:
            save(dest.replace(".png", "-front.png"), blank())


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


def composite_stack(
    *,
    background: str,
    base: str,
    block: str | None = None,
    body: str | None = None,
    hat: str | None = None,
    accessory: str | None = None,
) -> Image.Image:
    """Studio/generator order: clothes wrap the neck, wall clips the chest, paws on the ledge."""
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
    comp(block or "base/wall-default.png")
    if body:
        comp(body.replace(".png", "-front.png"))
    if acc_id in LEDGE_ACCESSORIES:
        comp(accessory)
    comp(f"base/front-paws-{color}.png")
    return canvas


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
